%{?_javapackages_macros:%_javapackages_macros}

Name:           libmatthew-java
Version:        0.8
Release:        15.1
Summary:        A few useful Java libraries
Group:          Development/Libraries
License:        MIT

# actual upstream:
URL: http://matthew.ath.cx/projects/java/
Source0: http://matthew.ath.cx/projects/java/%{name}-%{version}.tar.gz

# OSGi manifests
Source1:        %{name}-hexdump-osgi-MANIFEST.MF
Source2:        %{name}-unix-osgi-MANIFEST.MF

Patch0:         install_doc.patch
Patch1:         native-library-paths.patch
Patch2:         classpath_fix.patch

BuildRequires:  java-devel >= 1:1.6.0

Requires:       java-headless
Requires:       javapackages-tools

%description
A colleciton of Java libraries:
- Unix Sockets Library
  This is a collection of classes and native code to allow you to read
  and write Unix sockets in Java.

- Debug Library
  This is a comprehensive logging and debugging solution.

- CGI Library
  This is a collection of classes and native code to allow you to write
  CGI applications in Java.

- I/O Library
  This provides a few much needed extensions to the Java I/O subsystem.

- Hexdump
  This class formats byte-arrays in hex and ascii for display.


%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Libraries
Requires:       javapackages-tools


%description javadoc
Javadoc for %{name}


%prep
%setup -q
%patch0 -p1

# this patch adds a system dependent path, so we fix it before
# applying the patch
sed -e 's|@JNIPATH@|%{_libdir}/%{name}|' %{PATCH1} | patch -p1 

%patch2 -p1


%build
export JAVA_HOME=%{java_home}
make %{?_smp_mflags} \
    CFLAGS='%{optflags}'\
    GCJFLAGS='%{optflags}' \
    LDFLAGS='%{optflags}' \
    PPFLAGS='%{optflags}' \
    JAVADOC="javadoc -Xdoclint:none" \
    -j1

# Inject OSGi manifests
jar umf %{SOURCE1} hexdump-0.2.jar
jar umf %{SOURCE2} unix-0.5.jar

%install
make install \
    DESTDIR=$RPM_BUILD_ROOT \
    JARDIR=%{_jnidir} \
    LIBDIR=%{_libdir}/%{name} \
    DOCDIR=%{_javadocdir}/%{name} \
    JAVADOC="javadoc -Xdoclint:none"

%files
%{_jnidir}/*.jar
%{_libdir}/%{name}
%doc COPYING INSTALL README

%files javadoc
%{_javadocdir}/%{name}
%doc COPYING


%changelog
* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.8-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.8-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jun 22 2015 Omair Majid <omajid@redhat.com> 0.8-13
- Require javapackages-tools, not jpackage-utils.

* Thu Jun 18 2015 Alexander Kurtakov <akurtako@redhat.com> 0.8-12
- Fix FTBFS - disable strict doclint.

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Feb 24 2014 Omair Majid <omajid@redhat.com> 0.8-8
- Require java-headless

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 5 2013 Alexander Kurtakov <akurtako@redhat.com> 0.8-6
- Place jars in _jnidir according to new guidelines.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Oct 11 2011 Omair Majid <omajid@redhat.com> 0.8-2
- Add patch to replace System.loadLibrary with System.load with explicit paths

* Wed Jun 29 2011 Alexander Kurtakov <akurtako@redhat.com> 0.8-1
- Update to new upstream version (0.8).
- License changed to MIT.

* Sun Feb 13 2011 Mat Booth <fedora@matbooth.co.uk> 0.7.2-5
- Inject OSGi manifests into jars so that they may be used in OSGi apps such
  as Eclipse plug-ins.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jul 8 2010 Omair Majid <omajid@redhat.com> 0.7.2-3
- Add license file to javadoc subpackage

* Wed Jan 13 2010 Alexander Kurtakov <akurtako@redhat.com> 0.7.2-2
- Export JAVA_HOME to fix build.

* Wed Jan 13 2010 Alexander Kurtakov <akurtako@redhat.com> 0.7.2-1
- Update to upstream 0.7.2.
- Drop gcj_support.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Sep 4 2008 Omair Majid <omajid@redhat.com> 0.7.1-4
- Added -j1 to disable parallel build. Fixes the race condition that resulted 
  in class files of size 0
- Eliminated early_upstream.patch (patch was adapted by upstream)

* Thu Aug 28 2008 Omair Majid <omajid@redhat.com> 0.7.1-3
- Created new patches that dont cause fuzz when patching.

* Wed Jul 2 2008 Omair Majid <omajid@redhat.com> 0.7.1-2
- Fixed hardcoded paths for jni libraries

* Wed Jun 25 2008 Omair Majid <omajid@redhat.com> 0.7.1-1.fc9
- Initial build for fedora
