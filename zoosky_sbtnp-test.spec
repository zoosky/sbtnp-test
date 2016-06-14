Name: zoosky_sbtnp-test
Version: 1.0.0
Release: 2
Summary: sbtnp-test summary
prefix: /appl
License: None
Vendor: sbtnp-test vendor
URL: http://www.example.com/
AutoProv: yes
AutoReq: yes
BuildRoot: /home/andreas/dev/sbtnp-test/target/rpm/buildroot
BuildArch: noarch

%description
sbtnp-test description


%install
if [ -e "$RPM_BUILD_ROOT" ]; then
  mv "/home/andreas/dev/sbtnp-test/target/rpm/tmp-buildroot"/* "$RPM_BUILD_ROOT"
else
  mv "/home/andreas/dev/sbtnp-test/target/rpm/tmp-buildroot" "$RPM_BUILD_ROOT"
fi

%pretrans
# pretrans
#-------------



%pre
# pre
#-------------

# Adding system user/group : sbtnp and sbtnp
if ! getent group | grep -q "^sbtnp:" ;
then
    echo "Creating system group: sbtnp"
    groupadd -g 1267 sbtnp
fi
if ! getent passwd | grep -q "^sbtnp:"; 
then
    echo "Creating system user: sbtnp"
    #useradd -u 6826 sbtnp --system -c 'sbtnp-test summary' sbtnp
    useradd -u 6826 -c 'sbtnp-test summary' -d /home/sbtnp -m -g sbtnp -G sbtnp,users sbtnp

fi

# pre
#-------------

# Adding system user/group : sbtnp and sbtnp
if ! getent group | grep -q "^sbtnp:" ;
then
    echo "Creating system group: sbtnp"
    groupadd -g 1267 sbtnp
fi
if ! getent passwd | grep -q "^sbtnp:"; 
then
    echo "Creating system user: sbtnp"
    #useradd -u 6826 sbtnp --system -c 'sbtnp-test summary' sbtnp
    useradd -u 6826 -c 'sbtnp-test summary' -d /home/sbtnp -m -g sbtnp -G sbtnp,users sbtnp

fi



%post
#post
#-------------

# PROFILE
echo 'export JAVA_HOME=/appl/sbtnp-test/jdk.latest'>> /home/sbtnp/.profile
echo 'export PATH=$JAVA_HOME/bin:$PATH' >> /home/sbtnp/.profile

# JDK
ln -s /appl/cngjava/oracle/jdk1.8.0_77 /appl/sbtnp-test/jdk.latest


chmod +x /etc/init.d/sbtnp-test
chkconfig sbtnp-test on

rm -r /appl/sbtnp-test/crx-quickstart/logs

# echo 'Symbolischen Links setzen'
ln -sf /userlogs/sbtnp-test/ /appl/sbtnp-test/crx-quickstart/logs
ln -sf /data/sbtnp-test/repository /appl/sbtnp-test/crx-quickstart/repository 


chown sbtnp.sbtnp -R /appl/sbtnp-test
chmod -R 775 /appl/sbtnp-test
chown sbtnp.sbtnp -R /data/sbtnp-test
chmod -R 775 /data/sbtnp-test

#post
#-------------

# PROFILE
echo 'export JAVA_HOME=/appl/sbtnp-test/jdk.latest'>> /home/sbtnp/.profile
echo 'export PATH=$JAVA_HOME/bin:$PATH' >> /home/sbtnp/.profile

# JDK
ln -s /appl/cngjava/oracle/jdk1.8.0_77 /appl/sbtnp-test/jdk.latest


chmod +x /etc/init.d/sbtnp-test
chkconfig sbtnp-test on

rm -r /appl/sbtnp-test/crx-quickstart/logs

# echo 'Symbolischen Links setzen'
ln -sf /userlogs/sbtnp-test/ /appl/sbtnp-test/crx-quickstart/logs
ln -sf /data/sbtnp-test/repository /appl/sbtnp-test/crx-quickstart/repository 


chown sbtnp.sbtnp -R /appl/sbtnp-test
chmod -R 775 /appl/sbtnp-test
chown sbtnp.sbtnp -R /data/sbtnp-test
chmod -R 775 /data/sbtnp-test



%verifyscript
# verifyscript
#-------------



%posttrans
# posttrans
#-------------



%preun
# preun
#-------------

# Halting sbtnp-test

echo "Shutdown sbtnp-test"
%stop_on_removal sbtnp-test
/etc/init.d/sbtnp-test stop

(cd /appl && tar cf - sbtnp-test) > /data/backup-appl-sbtnp-test.tar
(cd /data && tar cf - sbtnp-test) > /data/backup-data-sbtnp-test.tar

# preun
#-------------

# Halting sbtnp-test

echo "Shutdown sbtnp-test"
%stop_on_removal sbtnp-test
/etc/init.d/sbtnp-test stop

(cd /appl && tar cf - sbtnp-test) > /data/backup-appl-sbtnp-test.tar
(cd /data && tar cf - sbtnp-test) > /data/backup-data-sbtnp-test.tar



%postun
#postun
#-------------

rm -r /appl/sbtnp-test
rm -r /userlogs/sbtnp-test

# Removing system user/group : sbtnp and sbtnp
echo "Try deleting system user and group [sbtnp:sbtnp]"
if getent passwd | grep -q "^sbtnp:"; 
then
    echo "Deleting system user: sbtnp"
    userdel -r sbtnp
fi
if getent group | grep -q "^sbtnp:" ;
then
    echo "Deleting system group: sbtnp"
    groupdel sbtnp
fi

#postun
#-------------

rm -r /appl/sbtnp-test
rm -r /userlogs/sbtnp-test

# Removing system user/group : sbtnp and sbtnp
echo "Try deleting system user and group [sbtnp:sbtnp]"
if getent passwd | grep -q "^sbtnp:"; 
then
    echo "Deleting system user: sbtnp"
    userdel -r sbtnp
fi
if getent group | grep -q "^sbtnp:" ;
then
    echo "Deleting system group: sbtnp"
    groupdel sbtnp
fi



%files
%attr(775,sbtnp,sbtnp) /appl/sbtnp-test/crx-quickstart/bin/quickstart
%attr(775,sbtnp,sbtnp) /appl/sbtnp-test/crx-quickstart/bin/start
%attr(775,sbtnp,sbtnp) /appl/sbtnp-test/crx-quickstart/bin/status
%attr(775,sbtnp,sbtnp) /appl/sbtnp-test/crx-quickstart/bin/stop
%dir %attr(775,sbtnp,sbtnp) /appl/sbtnp-test/crx-quickstart
%dir %attr(775,sbtnp,sbtnp) /appl/sbtnp-test/crx-quickstart/bin
%dir %attr(775,sbtnp,sbtnp) /appl/sbtnp-test/crx-quickstart/logs
%dir %attr(775,sbtnp,sbtnp) /appl/sbtnp-test/crx-quickstart/repository
%attr(775,sbtnp,sbtnp) /appl/sbtnp-test/crx-quickstart/readme.txt
%attr(775,sbtnp,sbtnp) /appl/sbtnp-test/crx-quickstart/logs/logdir.txt
%attr(775,sbtnp,sbtnp) /appl/sbtnp-test/crx-quickstart/repository/repodir.txt
%dir %attr(775,sbtnp,sbtnp) /userlogs/sbtnp-test
%dir %attr(775,sbtnp,sbtnp) /data/sbtnp-test/repository
%dir %attr(775,sbtnp,sbtnp) /usertmp/aem-work
%config %attr(644,root,root) /appl/sbtnp-test/sbtnp-test.config
%dir %attr(755,sbtnp,sbtnp) /var/run/zoosky_sbtnp-test
%attr(0755,root,root) /etc/init.d/sbtnp-test
