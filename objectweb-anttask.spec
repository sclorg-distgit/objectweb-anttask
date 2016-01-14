%global pkg_name objectweb-anttask
%{?scl:%scl_package %{pkg_name}}
%{?maven_find_provides_and_requires}

# Copyright (c) 2000-2005, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%global _with_bootstrap 0

%global with_bootstrap %{!?_with_bootstrap:0}%{?_with_bootstrap:1}
%global without_bootstrap %{?_with_bootstrap:0}%{!?_with_bootstrap:1}


Summary:        ObjectWeb Ant task
Name:           %{?scl_prefix}%{pkg_name}
Version:        1.3.2
Release:        10.12%{?dist}
Epoch:          0
License:        LGPLv2+
URL:            http://forge.objectweb.org/projects/monolog/
BuildArch:      noarch
Source0:        http://download.forge.objectweb.org/monolog/ow_util_ant_tasks_1.3.2.zip
BuildRequires:  %{?scl_prefix_java_common}ant >= 0:1.6
BuildRequires:  %{?scl_prefix_java_common}javapackages-tools

%if %{without_bootstrap}
BuildRequires:  %{?scl_prefix}asm2
Requires:       %{?scl_prefix}asm2
%endif
Requires:       %{?scl_prefix_java_common}ant
%{?scl:Requires: %{scl_prefix}runtime}

%description
ObjectWeb Ant task

%package        javadoc
Summary:        Javadoc for %{pkg_name}

%description    javadoc
Javadoc for %{pkg_name}.

%prep
%setup -c -q -n %{pkg_name}
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x

# extract jars iff in bootstrap mode
%if %{without_bootstrap}
find . -name "*.class" -exec rm {} \;
find . -name "*.jar" -exec rm {} \;
%endif
%{?scl:EOF}

%build
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
export CLASSPATH=$(build-classpath asm2/asm2)
ant -Dbuild.compiler=modern -Dbuild.sysclasspath=first jar jdoc
%{?scl:EOF}

%install
%{?scl:scl enable %{scl} - <<"EOF"}
set -e -x
# jars
install -d -m 0755 $RPM_BUILD_ROOT%{_javadir}

install -m 644 output/lib/ow_util_ant_tasks.jar\
 $RPM_BUILD_ROOT%{_javadir}/%{pkg_name}.jar

# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -pr output/jdoc/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir_java_common}/ant.d
echo "%{pkg_name}" > $RPM_BUILD_ROOT%{_sysconfdir_java_common}/ant.d/%{pkg_name}
%{?scl:EOF}

%files
%doc doc/* 
%doc output/jdoc/*
%{_javadir}/*
%{_sysconfdir_java_common}/ant.d/*

%files javadoc
%doc %{_javadocdir}/%{name}

%changelog
* Fri Jan 16 2015 Michal Srb <msrb@redhat.com> - 0:1.3.2-10.12
- Add missing requires on maven30-runtime

* Thu Jan 15 2015 Michael Simacek <msimacek@redhat.com> - 0:1.3.2-10.11
- Install ant.d files into rh-java-common's ant.d

* Tue Jan 13 2015 Michael Simacek <msimacek@redhat.com> - 0:1.3.2-10.10
- Mass rebuild 2015-01-13

* Mon Jan 12 2015 Michael Simacek <msimacek@redhat.com> - 0:1.3.2-10.9
- BR/R on packages from rh-java-common

* Tue Jan 06 2015 Michael Simacek <msimacek@redhat.com> - 0:1.3.2-10.8
- Mass rebuild 2015-01-06

* Mon May 26 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.3.2-10.7
- Mass rebuild 2014-05-26

* Wed Feb 19 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.3.2-10.6
- Mass rebuild 2014-02-19

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.3.2-10.5
- Mass rebuild 2014-02-18

* Tue Feb 18 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.3.2-10.4
- Remove requires on java

* Mon Feb 17 2014 Michal Srb <msrb@redhat.com> - 0:1.3.2-10.3
- SCL-ize BR/R

* Thu Feb 13 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.3.2-10.2
- Rebuild to regenerate auto-requires

* Tue Feb 11 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.3.2-10.1
- First maven30 software collection build

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 01.3.2-10
- Mass rebuild 2013-12-27

* Fri Jun 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 0:1.3.2-9
- Rebuild to regenerate API documentation
- Resolves: CVE-2013-1571

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.3.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.3.2-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.3.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Sep 16 2011 Alexander Kurtakov <akurtako@redhat.com> 0:1.3.2-5
- Adapt to current guidelines.
- Properly integrate with ant using /etc/ant.d.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.3.2-4.5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jan 11 2010 Andrew Overholt <overholt@redhat.com> 0:1.3.2-3.5
- Fix Group tags
- Fix Source0 URL.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.3.2-3.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.3.2-2.4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jul  9 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 0:1.3.2-1.4
- drop repotag

* Thu May 29 2008 Tom "spot" Callaway <tcallawa@redhat.com> 0:1.3.2-1jpp.3
- fix license tag

* Wed Aug 29 2007 Deepak Bhole <dbhole@redhat.com> 0:1.3.2-1jpp.2
- Remove distribution tag

* Mon Feb 12 2007 Tania Bento <tbento@redhat.com> 0:1.3.2-1jpp.1
- Changed %%BuildRoot tag.
- Bootstrap Buildling.
- Should not touch buildroot in %%prep.
- Removed %%Vendor tag.
- Removed %%Distribution tag.
- Fixed %%Release tag.
- Fixed %%Sourcei0 tag.
- Added %%doc to %%files section.
- Edited %%doc in %%files javadoc section.

* Thu Jul 20 2006 Ralph Apel <r.apel at r-apel.de> 0:1.3.2-1jpp
- First JPP-1.7 release
- Upgrade to 1.3.2, now requires asm2
- Add javadoc subpackage

* Mon Sep 20 2004 Ralph Apel <r.apel at r-apel.de> 0:1.2-1jpp
- First JPackage release
