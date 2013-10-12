mkdir -p BUILD RPMS SOURCES SPECS SRPMS

/usr/bin/rpmbuild --buildroot `pwd`/BUILDROOT/ --define "_sourcedir `pwd`" --define "_rpmdir ./RPMS" --define "_buildir ." --define "_srcrpmdir ." --define "_speccdir ." --define "_topdir ." --define "_hash 12345" --define "_jobs 01" --define "_changelog 12345" -ba SPECS/rpmControler.spec
