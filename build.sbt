import NativePackagerHelper._
//import com.typesafe.sbt.packager.archetypes.ServerLoader
import com.typesafe.sbt.packager.linux.LinuxSymlink


lazy val root = (project in file(".")).
  settings(
// ----------------
    name := "sbtnp-test",
    version := "1.0.0",
// ----------------
    scalaVersion := "2.11.8",
    publishArtifact in (ThisBuild) := false
  )

enablePlugins(JavaServerAppPackaging, SystemVPlugin, RpmPlugin)
crossPaths := false
autoScalaLibrary := false


name in Linux  := name.value
version in Linux := version.value
maintainer in Linux := "zoosky at gmail.com"
packageSummary in Linux := "sbtnp-test summary"
packageDescription := "sbtnp-test description"


daemonUser in Linux := "sbtnp"
daemonUserUid in Linux := Option("6826")
daemonGroup in Linux := "sbtnp"
daemonGroupGid  in Linux := Option("1267")
daemonShell in Linux := "/bin/bash"
linuxStartScriptName in Linux := Option(name.value)
bashScriptEnvConfigLocation in Linux := Some(defaultLinuxInstallLocation.value + "/" + (name in Linux).value + "/" + (name in Linux).value + ".config")


//relocatable package
defaultLinuxInstallLocation := "/appl"
defaultLinuxLogsLocation := "/userlogs"
//defaultLinuxLogsLocation := defaultLinuxInstallLocation + "/" + name
defaultLinuxConfigLocation := "/appl" 
rpmPrefix := Option(defaultLinuxInstallLocation.value)
linuxPackageSymlinks := Seq.empty

// RPM
//serverLoading in Rpm := ServerLoader.SystemV
name in Rpm := name.value
packageName in Rpm := "zoosky_" + name.value
rpmRelease := "2"
rpmVendor := "sbtnp-test vendor"
rpmUrl := Some("http://www.example.com/")
rpmLicense := Some("None")

rpmBrpJavaRepackJars in Rpm := false
linuxStartScriptTemplate in Linux := (baseDirectory.value / "src" / "templates" / "rpm" / "start-rpm-template").asURL

linuxPackageSymlinks <<= (linuxPackageSymlinks) map (_ => Seq.empty[LinuxSymlink])

// Add an empty folder to mappings
linuxPackageMappings += packageTemplateMapping(s"/data/${name.value}/repository")()withUser((daemonUser in Linux).value) withGroup((daemonGroup in Linux).value)
linuxPackageMappings += packageTemplateMapping(s"/usertmp/${name.value}")()withUser((daemonUser in Linux).value) withGroup((daemonGroup in Linux).value)

mappings in Universal ++= contentOf("src/resources")

linuxPackageMappings in Linux := {
    // mappings: Seq[LinuxPackageMapping]
    val mappings = linuxPackageMappings.value
    
    mappings map {  linuxPackage =>
        // basic scala collections operations. Seq[(java.io.File, String)]
            
        val filtered = linuxPackage.mappings map {
            case (file, name) => file -> name // altering stuff here
        } filter {
            //case (file, name) => true // remove stuff from mappings
            case (file, name) => ! ((name.startsWith(name) && name.endsWith(".jar")) || file.getAbsolutePath.startsWith("/var/run"))
            //case (file, name) => ! (file.name == artfile.name)
            
        }
        // case class copy method. Specify only what you need
        val fileData = linuxPackage.fileData.copy(
            user = (daemonUser in Linux).value,
            group = (daemonGroup in Linux).value,
            permissions = "775",
            config = "false",
            docs = false
        )
        // case class copy method. Specify only what you need.
        // returns a fresh LinuxPackageMapping 
        linuxPackage.copy(
            mappings = filtered,
            fileData = fileData
        )
    } filter {
        linuxPackage => linuxPackage.mappings.nonEmpty // remove stuff. Here all empty linuxPackageMappings
    }
}

TaskKey[Unit]("linuxPkgMapppings") := {
  println("linuxPackageMappings")
  //val mapp = (linuxPackageMappings in Linux).value
  val mapp = linuxPackageMappings.value
    mapp map {  linuxPackage =>
        //println(linuxPackage)
        linuxPackage.mappings map { p => 
            println("p: " + p)
        }
  }
  val cwd = (stagingDirectory in Universal).value
  println(cwd)
}

val uniMappings = taskKey[Unit]("uniMappings") 

uniMappings := {
  (mappings in Universal).value
  //.filter(_._2 contains "jar")
  .foreach {
    case (file, path) => println(file + " -> " + path)
  }
}

TaskKey[Unit]("unzip") <<= (baseDirectory, packageBin in Rpm, streams) map { (baseDir, rpmFile, streams) =>
  val rpmPath = Seq(rpmFile.getAbsolutePath)
  Process("rpm2cpio" , rpmPath) #| Process("cpio -i --make-directories") ! streams.log
  ()
}


