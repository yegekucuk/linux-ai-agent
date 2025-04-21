import ollama
import os

# Function to check if given command is dangerous
def is_dangerous(command:str) -> bool:
    # Set lower case to avoid manupilating
    command = command.lower()
    # List of keywords identifying dangerous commands
    dangerous_keywords = [
        # Block any use of sudo
        "sudo", "su", "root",
        # These commands are banned
        "cd", "chmod", "chown", "exec","kill","pkill",
        # File & Directory Deletion
        "rm -rf", "rm -r", "rm -f", "rm --no-preserve-root", "rm *", "rm .*", "unlink", "del /f",
        "erase /f", "cryptsetup erase /dev/sda1",
        # Format & Partition Tools
        "mkfs", "mkfs.ext4", "mkfs.btrfs", "mkfs.xfs", "mkfs.vfat", 
        "parted", "fdisk", "cfdisk", "sgdisk", "sfdisk",
        # Disk Overwrite
        "dd if=", "dd of=", "/dev/sda", "/dev/sdb", "/dev/nvme", 
        "yes > /dev", "cat /dev/zero", "cat /dev/random", "wipefs", 
        # Destructive Redirects
        ">: /", ">:*", ">/dev/sda", ">/dev/null", "mv * /dev/null", 
        # Process & System Killers
        "kill -9 1", "kill -9 -- -1", "killall -9", "pkill -9", 
        ":(){", ":(){ :|:& };:", "fork bomb", 
        # Shutdown & Reboot Commands
        "shutdown", "reboot", "poweroff", "halt", 
        "init 0", "init 6", "systemctl reboot", "systemctl poweroff", 
        # Permission Changes
        "chmod 777 /", "chmod -r 777 /", "chmod -r 777", 
        "chown -r", "chgrp -r", "setfacl", 
        # Firewall & Network Tampering
        "iptables -f", "iptables --flush", "ufw disable", "ufw reset", 
        "firewalld stop", "nft flush", "ip route flush", 
        # User/Password File Destruction
        ">: /etc/passwd", ">: /etc/shadow", 
        "echo > /etc/passwd", "echo > /etc/shadow", 
        # System Integrity Destruction
        "ln -sf /dev/null", 
        "mv /bin", "mv /boot", "mv /etc", "mv /lib", "mv /usr", "mv /var",
        # Infinite Loops
        "while true; do", "for ((;;)); do", "yes |", 
        # Compression to Devices
        "tar cf /dev/sda", "gzip -c", "bzip2 -c", "xz -c", 
        # Bootloader / Mount Tampering
        "umount /", "mount /dev", "grub-install", "update-grub", 
        # History Tampering
        "history -c", "rm ~/.bash_history", "unset histfile", 
        # Secure Deletion Tools
        "shred", "wipe", "srm", "scrub",
        # Windows-style dangerous commands (cross-shell)
        "format c:", "format d:", "del c:\\", "rd /s /q", "rmdir /s /q",
        # Misc
        "ddrescue", "cryptsetup", "vgremove", "lvremove", "pvremove",
        "zpool destroy", "btrfs subvolume delete", "xfs_admin -d",
        # Protected directories
        " ~", " /", "/bin", "/sbin", "/lib", "/lib64", "/usr", "/usr/bin", "/usr/sbin", "/usr/lib", "/usr/lib64", 
        "/usr/local", "/usr/local/bin", "/usr/local/sbin", "/etc", "/etc/passwd", "/etc/shadow", "/etc/group", 
        "/etc/fstab", "/etc/hosts", "/etc/network", "/etc/ssh", "/etc/systemd", "/etc/init.d", "/etc/crontab", 
        "/etc/docker", "/etc/kubernetes", "/var", "/var/log", "/var/log/journal", "/var/spool", "/var/spool/cron", 
        "/var/spool/mail", "/var/lib", "/var/lib/docker", "/var/lib/kubelet", "/var/lib/etcd", "/var/cache", "/var/run", 
        "/var/lock", "/root", "/boot", "/dev", "/dev/sda*", "/dev/sdb*", "/dev/nvme*", "/dev/zero", "/dev/random", 
        "/dev/null", "/proc", "/sys", "/run", "/tmp", "/mnt", "/media", "/opt", "/srv", "/usr/share", "/run/docker.sock",
    ]
    # Return True if any dangerous keyword is found in the input command
    return any(danger in command for danger in dangerous_keywords)

def main():
    # Get the prompt
    prompt = input()
    # Take the command from the AI ​​model, the command in the model's response is extracted and cleaned
    response = ollama.generate(
            model='llama3-linuxassistant',
            prompt=prompt
        )
    command = response["response"]
    command = command.strip().strip("```").replace("bash", "").strip()
    print(command)
    
    try:
        # Raise an error if the command is dangerous
        if is_dangerous(command):
            raise ValueError("Dangerous commands are not run.")
        # Ask for validation
        validation = str(input("Type 'YES' to run the command: "))
        if validation == "YES":
            # Run the command
            os.system(f"echo '{command}' > linuxassistant.sh && chmod +x linuxassistant.sh && ./linuxassistant.sh")
        else:
            raise ValueError("Permission is not given.")
    except ValueError as ve:
        # Print the error
        print(ve)
    finally:
        # Delete the temporary created bash file
        os.system("rm linuxassistant.sh")

if __name__ == '__main__':
    main()