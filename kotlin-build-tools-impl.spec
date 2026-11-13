Name:		kotlin-build-tools-impl
Version:	2.4.21
Release:	1
Summary:	Kotlin build tools implementation
Group:		Development/Java
License:	Apache-2.0
URL:		https://github.com/JetBrains/kotlin
# Kotlin tag v2.4.21, compiler/build-tools/kotlin-build-tools-impl.
# Artifact org.jetbrains.kotlin:kotlin-build-tools-impl.
# kotlinc 2.0.21 compiles the 2.4 sources against the installed compiler jar.
# Patch0 keeps the 2.0 argument classes, compiles only the new wasm argument
# types, and sends flags that jar does not have through setUsingReflection.
# Wasm incremental compilation throws: KotlinWasmCompiler is not in 2.0.21.
# The Argument annotation overlay is compile-only and is not shipped.
# The scripting compiler embeddable is a build classpath only. Putting it on
# the runtime classpath registers a 2.4 plugin the 2.0 registrar cannot call.
Patch0:		kotlin-build-tools-impl-2.4.21-kotlinc20.patch
Source0:	kotlin-build-tools-impl-%{version}.tar.gz

BuildArch:	noarch
BuildRequires:	java-21-openjdk-devel
BuildRequires:	kotlin = 2.0.21
BuildRequires:	kotlin-stdlib >= 2.4.21-2
BuildRequires:	mvn(org.jetbrains.kotlin:kotlin-stdlib) = 2.4.21
BuildRequires:	mvn(org.jetbrains.kotlin:kotlin-reflect) = 2.4.21
BuildRequires:	mvn(org.jetbrains.kotlin:kotlin-build-tools-api) = 2.4.21
BuildRequires:	mvn(org.jetbrains.kotlin:kotlin-tooling-core) = 2.4.21
BuildRequires:	mvn(org.jetbrains.kotlin:kotlin-metadata-jvm) = 2.4.21
BuildRequires:	mvn(org.jetbrains.kotlin:kotlin-script-runtime) = 2.4.21
BuildRequires:	mvn(org.jetbrains.kotlin:kotlin-scripting-common) = 2.4.21
BuildRequires:	mvn(org.jetbrains.kotlin:kotlin-scripting-jvm) = 2.4.21
BuildRequires:	mvn(org.jetbrains.kotlin:kotlin-scripting-jvm-host) = 2.4.21
BuildRequires:	mvn(org.jetbrains.kotlin:kotlin-scripting-compiler-embeddable) = 2.4.21
BuildRequires:	mvn(org.jetbrains.kotlin:kotlin-scripting-compiler-impl-embeddable) = 2.4.21
BuildRequires:	mvn(org.jetbrains.kotlin:kotlin-compiler-runner) = 2.4.21
BuildRequires:	mvn(org.jetbrains.kotlin:kotlin-daemon-client) = 2.4.21
BuildRequires:	mvn(org.jetbrains.kotlin:jvm-abi-gen-embeddable) = 2.4.21
BuildRequires:	mvn(com.google.guava:guava)
BuildRequires:	mvn(com.google.code.gson:gson)
BuildRequires:	mvn(io.github.java-diff-utils:java-diff-utils)
BuildRequires:	sysjar
BuildRequires:	javapackages-filesystem
Requires:	kotlin = 2.0.21
Requires:	mvn(org.jetbrains.kotlin:kotlin-stdlib) = 2.4.21
Requires:	mvn(org.jetbrains.kotlin:kotlin-reflect) = 2.4.21
Requires:	mvn(org.jetbrains.kotlin:kotlin-build-tools-api) = 2.4.21
Requires:	mvn(org.jetbrains.kotlin:kotlin-tooling-core) = 2.4.21
Requires:	mvn(org.jetbrains.kotlin:kotlin-metadata-jvm) = 2.4.21
Requires:	mvn(org.jetbrains.kotlin:kotlin-script-runtime) = 2.4.21
Requires:	mvn(org.jetbrains.kotlin:kotlin-scripting-common) = 2.4.21
Requires:	mvn(org.jetbrains.kotlin:kotlin-scripting-jvm) = 2.4.21
Requires:	mvn(org.jetbrains.kotlin:kotlin-scripting-jvm-host) = 2.4.21
Requires:	mvn(org.jetbrains.kotlin:kotlin-compiler-runner) = 2.4.21
Requires:	mvn(org.jetbrains.kotlin:kotlin-daemon-client) = 2.4.21
Requires:	mvn(org.jetbrains.kotlin:jvm-abi-gen-embeddable) = 2.4.21
Requires:	mvn(com.google.guava:guava)
Requires:	mvn(com.google.code.gson:gson)
Requires:	mvn(io.github.java-diff-utils:java-diff-utils)

%description
org.jetbrains.kotlin:kotlin-build-tools-impl %{version}.
The build-tools implementation from Kotlin tag v2.4.21, compiled with the
installed kotlinc 2.0.21 against that release's compiler jar.

%prep
%autosetup -n kotlin-build-tools-impl-%{version} -p1
find . -type f \( -name '*.jar' -o -name '*.class' -o -name '*.so' -o -name '*.node' -o -name '*.wasm' \) -print > binaries.list
if [ -s binaries.list ]; then
	cat binaries.list
	exit 1
fi

%build
set -eo pipefail
export JAVA_HOME=%{_jvmdir}/java-21-openjdk
export PATH="$JAVA_HOME/bin:/usr/bin:/bin"
export STDLIB=%{_javadir}/kotlin-stdlib-%{version}.jar
export REFLECT=%{_javadir}/kotlin-reflect-%{version}.jar
export API=%{_javadir}/kotlin-build-tools-api.jar
export TOOLING=%{_javadir}/kotlin-tooling-core.jar
export METADATA=%{_javadir}/kotlin-metadata-jvm.jar
export RUNTIME=%{_javadir}/kotlin-script-runtime-%{version}.jar
export COMMON=%{_javadir}/kotlin-scripting-common.jar
export SJVM=%{_javadir}/kotlin-scripting-jvm.jar
export HOST=%{_javadir}/kotlin-scripting-jvm-host.jar
export PLUGIN=%{_javadir}/kotlin-scripting-compiler-embeddable.jar
export PLUGIN_IMPL=%{_javadir}/kotlin-scripting-compiler-impl-embeddable.jar
export RUNNER=%{_javadir}/kotlin-compiler-runner.jar
export DAEMON=%{_javadir}/kotlin-daemon-client.jar
export ABI=%{_javadir}/jvm-abi-gen-embeddable.jar
export GUAVA=/usr/share/java/guava.jar
export GSON=/usr/share/java/gson.jar
export DIFF=/usr/share/java/java-diff-utils.jar
export ANNO=/usr/share/kotlin/lib/annotations-13.0.jar
export COMPILER=/usr/share/kotlin/lib/kotlin-compiler.jar
bash tools/compile.sh
cat > kotlin-build-tools-impl.pom << END
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0">
  <modelVersion>4.0.0</modelVersion>
  <groupId>org.jetbrains.kotlin</groupId>
  <artifactId>kotlin-build-tools-impl</artifactId>
  <version>%{version}</version>
  <name>kotlin-build-tools-impl</name>
  <description>Kotlin build tools implementation</description>
  <url>https://github.com/JetBrains/kotlin</url>
  <licenses>
    <license>
      <name>Apache-2.0</name>
      <url>https://www.apache.org/licenses/LICENSE-2.0.txt</url>
    </license>
  </licenses>
  <dependencies>
    <dependency>
      <groupId>org.jetbrains.kotlin</groupId>
      <artifactId>kotlin-stdlib</artifactId>
      <version>%{version}</version>
    </dependency>
    <dependency>
      <groupId>org.jetbrains.kotlin</groupId>
      <artifactId>kotlin-reflect</artifactId>
      <version>%{version}</version>
    </dependency>
    <dependency>
      <groupId>org.jetbrains.kotlin</groupId>
      <artifactId>kotlin-build-tools-api</artifactId>
      <version>%{version}</version>
    </dependency>
    <dependency>
      <groupId>org.jetbrains.kotlin</groupId>
      <artifactId>kotlin-tooling-core</artifactId>
      <version>%{version}</version>
    </dependency>
    <dependency>
      <groupId>org.jetbrains.kotlin</groupId>
      <artifactId>kotlin-metadata-jvm</artifactId>
      <version>%{version}</version>
    </dependency>
    <dependency>
      <groupId>org.jetbrains.kotlin</groupId>
      <artifactId>kotlin-script-runtime</artifactId>
      <version>%{version}</version>
    </dependency>
    <dependency>
      <groupId>org.jetbrains.kotlin</groupId>
      <artifactId>kotlin-scripting-common</artifactId>
      <version>%{version}</version>
    </dependency>
    <dependency>
      <groupId>org.jetbrains.kotlin</groupId>
      <artifactId>kotlin-scripting-jvm</artifactId>
      <version>%{version}</version>
    </dependency>
    <dependency>
      <groupId>org.jetbrains.kotlin</groupId>
      <artifactId>kotlin-scripting-jvm-host</artifactId>
      <version>%{version}</version>
    </dependency>
    <dependency>
      <groupId>org.jetbrains.kotlin</groupId>
      <artifactId>kotlin-compiler-runner</artifactId>
      <version>%{version}</version>
    </dependency>
    <dependency>
      <groupId>org.jetbrains.kotlin</groupId>
      <artifactId>kotlin-daemon-client</artifactId>
      <version>%{version}</version>
    </dependency>
    <dependency>
      <groupId>org.jetbrains.kotlin</groupId>
      <artifactId>jvm-abi-gen-embeddable</artifactId>
      <version>%{version}</version>
    </dependency>
  </dependencies>
</project>
END

%install
set -eo pipefail
sysjar install --buildroot %{buildroot} \
	--artifact kotlin-build-tools-impl.pom:kotlin-build-tools-impl.jar \
	--file-name kotlin-build-tools-impl \
	--filelist .mfiles
idx="%{buildroot}/usr/share/sysjar/index/org.jetbrains.kotlin/kotlin-build-tools-impl.sysjar"
test -s "$idx"
grep -F -q '"version": "%{version}"' "$idx"
grep -F -q '"artifactId": "kotlin-build-tools-impl"' "$idx"
grep -F -q '/usr/share/java/kotlin-build-tools-impl.jar' "$idx"
test -s %{buildroot}%{_javadir}/kotlin-build-tools-impl.jar

%check
set -eo pipefail
export JAVA_HOME=%{_jvmdir}/java-21-openjdk
export PATH="$JAVA_HOME/bin:/usr/bin:/bin"
export JAR=%{buildroot}%{_javadir}/kotlin-build-tools-impl.jar
export STDLIB=%{_javadir}/kotlin-stdlib-%{version}.jar
export REFLECT=%{_javadir}/kotlin-reflect-%{version}.jar
export API=%{_javadir}/kotlin-build-tools-api.jar
export TOOLING=%{_javadir}/kotlin-tooling-core.jar
export METADATA=%{_javadir}/kotlin-metadata-jvm.jar
export RUNTIME=%{_javadir}/kotlin-script-runtime-%{version}.jar
export COMMON=%{_javadir}/kotlin-scripting-common.jar
export SJVM=%{_javadir}/kotlin-scripting-jvm.jar
export HOST=%{_javadir}/kotlin-scripting-jvm-host.jar
export RUNNER=%{_javadir}/kotlin-compiler-runner.jar
export DAEMON=%{_javadir}/kotlin-daemon-client.jar
export ABI=%{_javadir}/jvm-abi-gen-embeddable.jar
export GUAVA=/usr/share/java/guava.jar
export GSON=/usr/share/java/gson.jar
export DIFF=/usr/share/java/java-diff-utils.jar
export ANNO=/usr/share/kotlin/lib/annotations-13.0.jar
export COMPILER=/usr/share/kotlin/lib/kotlin-compiler.jar
bash tools/check.sh
cat check/out.txt

%files -f .mfiles
%license license/LICENSE.txt
%doc license/NOTICE.txt
