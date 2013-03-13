%define gcj_support 0
%define	name	jrefactory
%define	version	2.8.9
%define	release	4.6.4
%define	section	free

Name:		%{name}
Version:	%{version}
Release:	%{release}
Epoch:		0
Summary:	JRefactory and Pretty Print
License:	Apache License
Group:		Development/Java
Source0:	%{name}-%{version}-full-RHCLEAN.zip
Patch0:		%{name}-pr21880.patch
Patch1:		%{name}-htmleditorkit.patch
Patch2:		%{name}-savejpg.patch
Patch3:		%{name}-2.8.9-fixcrlf.patch
Url:		http://jrefactory.sourceforge.net/
BuildRequires:	java-rpmbuild >= 0:1.5
BuildRequires:	ant
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
BuildArch:	noarch
%endif
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
JRefactory provides a variety of refactoring and pretty printing tools

%prep
%setup -q -c -n %{name}
mv settings/.Refactory settings/sample
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p0
rm -f src/org/acm/seguin/pmd/swingui/PMDLookAndFeel.java
%remove_java_binaries

# remove classes that don't build without said jarfiles
find -name '*.java' | \
    xargs grep -l '^import \(edu\|org\.\(jaxen\|saxpath\)\)\.' | \
        xargs rm

%build
perl -p -i -e 's|^Class-Path:.*||' \
	src/meta-inf/refactory.mf
%ant -Dant.build.javac.source=1.4 jar

%install
# jar
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
install -m 644 ant.build/lib/%{name}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-%{version}.jar

(cd $RPM_BUILD_ROOT%{_javadir} && for jar in *-%{version}.jar; do ln -sf ${jar} ${jar/-%{version}/}; done)

%if %{gcj_support}
aot-compile-rpm
%endif

for i in docs/{*.html,*.jpg,*.gif,*.txt} settings/sample/*; do
  %{__perl} -pi -e 's/\r$//g' $i
done

%clean
rm -rf $RPM_BUILD_ROOT

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%defattr(0664,root,root,0755)
%doc docs/{*.html,*.jpg,*.gif,*.txt} settings/sample
%{_javadir}/*
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/%{name}-%{version}.jar.*
%endif




%changelog
* Wed May 04 2011 Oden Eriksson <oeriksson@mandriva.com> 0:2.8.9-4.6.3mdv2011.0
+ Revision: 665835
- mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 0:2.8.9-4.6.2mdv2011.0
+ Revision: 606111
- rebuild

* Wed Mar 17 2010 Oden Eriksson <oeriksson@mandriva.com> 0:2.8.9-4.6.1mdv2010.1
+ Revision: 523108
- rebuilt for 2010.1

* Fri Jan 25 2008 Alexander Kurtakov <akurtakov@mandriva.org> 0:2.8.9-4.6.0mdv2008.1
+ Revision: 157968
- fix build

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

  + Anssi Hannula <anssi@mandriva.org>
    - buildrequire java-rpmbuild, i.e. build with icedtea on x86(_64)

* Sat Sep 15 2007 Anssi Hannula <anssi@mandriva.org> 0:2.8.9-4.5mdv2008.0
+ Revision: 87439
- rebuild to filter out autorequires of GCJ AOT objects
- remove unnecessary Requires(post) on java-gcj-compat

* Sun Sep 09 2007 Pascal Terjan <pterjan@mandriva.org> 0:2.8.9-4.4mdv2008.0
+ Revision: 82840
- rebuild


* Thu Mar 15 2007 Christiaan Welvaart <spturtle@mandriva.org> 2.8.9-4.3mdv2007.1
+ Revision: 144252
- rebuild for 2007.1
- Import jrefactory

* Sun Jun 04 2006 David Walluck <walluck@mandriva.org> 0:2.8.9-4.2mdv2007.0
- rebuild for libgcj.so.7
- own %%{_libdir}/gcj/%%{name}

* Fri Dec 02 2005 David Walluck <walluck@mandriva.org> 0:2.8.9-4.1mdk
- sync with 4jpp
- aot-compile

* Sun Sep 11 2005 David Walluck <walluck@mandriva.org> 0:2.8.9-3.1mdk
- release

* Thu Jun 16 2005 Gary Benson <gbenson@redhat.com> - 0:2.8.9-3jpp_1fc
- Build into Fedora.

* Thu Jun 09 2005 Gary Benson <gbenson@redhat.com>
- Remove jarfiles from the tarball.
- Remove classes that don't build without said jarfiles.

* Fri Jun 03 2005 Gary Benson <gbenson@redhat.com>
- Avoid some API holes in libgcj's Swing implementation.
- Avoid Sun-specific classes.

* Sat Oct 16 2004 Fernando Nasser <fnasser@redhat.com> - 0:2.8.9-3jpp_1rh
- First Red Hat build

* Tue Aug 24 2004 Randy Watler <rwatler at finali.com> - 0:2.8.9-3jpp
- Rebuild with ant-1.6.2

* Wed Jun 02 2004 Randy Watler <rwatler at finali.com> - 0:2.8.9-2jpp
- Upgrade to Ant 1.6.X

