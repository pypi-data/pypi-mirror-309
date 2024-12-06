import os
import subprocess
import shutil
import platform
from PIL import Image
import pefile
import struct
from jkpackager.metadata import PackageMetadata
def main():
    class JkPackager:
        def __init__(self, script_path, icon_path=None):
            self.script_path = script_path
            self.icon_path = icon_path
        if not os.path.isfile(self.script_path):
            raise FileNotFoundError(f"Script file '{self.script_path}' not found.")
        if self.icon_path and not os.path.isfile(self.icon_path):
            raise FileNotFoundError(f"Icon file '{self.icon_path}' not found.")
        
    def test_script(self):
        """Test the script to ensure it runs without errors."""
        print("Testing script...")
        result = subprocess.run(["python", self.script_path], capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"Script failed to run. Error:\n{result.stderr}")
        print("Script test passed.")
        
    def convert_icon_to_ico(self):
        """Convert the given icon file to a proper ICO format (if not already)."""
        try:
            img = Image.open(self.icon_path)
            if img.format != "ICO":
                print("Converting the icon to ICO format...")
                ico_path = self.icon_path.replace(".", "_converted.") + "ico"
                img.save(ico_path, format="ICO")
                return ico_path
            return self.icon_path
        except Exception as e:
            raise ValueError(f"Failed to process icon file: {e}")

    def embed_icon(self, exe_path):
        """Embed the icon into the .exe file."""
        if platform.system() != "Windows":
            print("Icon embedding is only supported on Windows.")
            return

        ico_path = self.convert_icon_to_ico()
        try:
            print(f"Embedding icon {ico_path} into {exe_path}...")
            pe = pefile.PE(exe_path)

            # Load the ICO file and extract its binary data
            with open(ico_path, "rb") as ico_file:
                ico_data = ico_file.read()

            # Find the resource table in the executable
            resource_section = None
            for section in pe.sections:
                if b".rsrc" in section.Name:
                    resource_section = section
                    break

            if not resource_section:
                raise RuntimeError("Resource section not found in the executable.")

            # Define the structure for embedding
            resource_offset = resource_section.PointerToRawData
            resource_rva = resource_section.VirtualAddress

            # Insert the ICO as a resource (ID 1, group icon ID 1)
            icon_entry = struct.pack("<HHHH", 1, 1, 0, len(ico_data))
            pe.set_bytes_at_offset(resource_offset, icon_entry + ico_data)
            pe.write(exe_path)

            print(f"Icon embedded successfully into {exe_path}!")
        except Exception as e:
            print(f"Failed to embed icon: {e}")

    def package_exe(self, output_folder):
        """Package as .exe (Windows)."""
        print("Packaging .exe...")
        exe_name = os.path.splitext(os.path.basename(self.script_path))[0] + ".exe"
        exe_path = os.path.join(output_folder, exe_name)

        # Basic conversion to .exe using a launcher script
        launcher_content = f"""
        @echo off
        python "{os.path.basename(self.script_path)}" %*
        """
        with open(exe_path, "w") as f:
            f.write(launcher_content)

        # Embed icon into the .exe file
        if self.icon_path:
            self.embed_icon(exe_path)
        
        print(f"Packaged .exe at {exe_path}")

    def package_pkg(self, output_folder):
        """Package as .pkg (macOS)."""
        print("Packaging .pkg...")
        pkg_name = os.path.splitext(os.path.basename(self.script_path))[0] + ".pkg"
        pkg_path = os.path.join(output_folder, pkg_name)

        # Mocking .pkg creation
        shutil.copy(self.script_path, pkg_path)
        print(f"Packaged .pkg at {pkg_path}")

    def package_deb(self, output_folder):
        """Package as .deb (Debian-based Linux)."""
        print("Packaging .deb...")
        deb_name = os.path.splitext(os.path.basename(self.script_path))[0] + ".deb"
        deb_path = os.path.join(output_folder, deb_name)

        # Mock .deb structure with control file
        os.makedirs(deb_path, exist_ok=True)
        control_content = f"""
        Package: {self.metadata.name}
        Version: {self.metadata.version}
        Section: base
        Priority: optional
        Architecture: all
        Maintainer: {self.metadata.author}
        Description: {self.metadata.description}
        """
        with open(os.path.join(deb_path, "control"), "w") as f:
            f.write(control_content)

        shutil.copy(self.script_path, deb_path)
        print(f"Packaged .deb at {deb_path}")

    def package_rpm(self, output_folder):
        """Package as .rpm (Red Hat-based Linux)."""
        print("Packaging .rpm...")
        rpm_name = os.path.splitext(os.path.basename(self.script_path))[0] + ".rpm"
        rpm_path = os.path.join(output_folder, rpm_name)

        # Mock .rpm structure with SPEC file
        os.makedirs(rpm_path, exist_ok=True)
        spec_content = f"""
        Name: {self.metadata.name}
        Version: {self.metadata.version}
        Release: 1%{{?dist}}
        Summary: {self.metadata.description}
        License: MIT
        Source0: {self.script_path}
        """
        with open(os.path.join(rpm_path, f"{self.metadata.name}.spec"), "w") as f:
            f.write(spec_content)

        shutil.copy(self.script_path, rpm_path)
        print(f"Packaged .rpm at {rpm_path}")

    def run(self, output_base="output"):
        """Run the full packaging process."""
        self.test_script()
        os.makedirs(output_base, exist_ok=True)

        self.package_exe(os.path.join(output_base, "exe"))
        self.package_pkg(os.path.join(output_base, "macos"))
        self.package_deb(os.path.join(output_base, "deb"))
        self.package_rpm(os.path.join(output_base, "rpm"))
        main()