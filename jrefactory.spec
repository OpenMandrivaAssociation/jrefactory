%define gcj_support 1
%define	name	jrefactory
%define	version	2.8.9
%define	release	%mkrel 4.6
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

# clean jarfiles
find . -name "*.jar" -exec rm -f {} \;

# remove classes that don't build without said jarfiles
find -name '*.java' | \
    xargs grep -l '^import \(edu\|org\.\(jaxen\|saxpath\)\)\.' | \
        xargs rm

%build
perl -p -i -e 's|^Class-Path:.*||' \
	src/meta-inf/refactory.mf
%ant jar

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


