%define gcj_support 0
%define	section	free

Summary:	JRefactory and Pretty Print
Name:		jrefactory
Version:	2.8.9
Release:	12
License:	Apache License
Group:		Development/Java
Url:		https://jrefactory.sourceforge.net/
Source0:	%{name}-%{version}-full-RHCLEAN.zip
Patch0:		%{name}-pr21880.patch
Patch1:		%{name}-htmleditorkit.patch
Patch2:		%{name}-savejpg.patch
Patch3:		%{name}-2.8.9-fixcrlf.patch

%if !%{gcj_support}
BuildArch:	noarch
%else
BuildRequires:  java-gcj-compat-devel
%endif
BuildRequires:	ant
BuildRequires:	java-rpmbuild >= 0:1.5

%description
JRefactory provides a variety of refactoring and pretty printing tools

%prep
%setup -q -c -n %{name}
mv settings/.Refactory settings/sample
%autopatch -p1
rm -f src/org/acm/seguin/pmd/swingui/PMDLookAndFeel.java
%remove_java_binaries

# remove classes that don't build without said jarfiles
find -name '*.java' | \
    xargs grep -l '^import \(edu\|org\.\(jaxen\|saxpath\)\)\.' | \
        xargs rm

%build
sed -i -e 's|^Class-Path:.*||' \
	src/meta-inf/refactory.mf
%ant -Dant.build.javac.source=1.4 jar

%install
# jar
install -d -m 755 %{buildroot}%{_javadir}
install -m 644 ant.build/lib/%{name}.jar %{buildroot}%{_javadir}/%{name}-%{version}.jar

(cd %{buildroot}%{_javadir} && for jar in *-%{version}.jar; do ln -sf ${jar} ${jar/-%{version}/}; done)

%if %{gcj_support}
aot-compile-rpm
%endif

for i in docs/{*.html,*.jpg,*.gif,*.txt} settings/sample/*; do
	sed -i -e 's/\r$//g' $i
done

%if %{gcj_support}
%post
%update_gcjdb

%postun
%clean_gcjdb
%endif

%files
%doc docs/{*.html,*.jpg,*.gif,*.txt} settings/sample
%{_javadir}/*
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/%{name}-%{version}.jar.*
%endif

