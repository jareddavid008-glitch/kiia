SAFE_WMIC_COMMANDS = {
    "System": {
        "Operating System": ["os", "get", "Caption,Version,BuildNumber"],
        "Computer System": ["computersystem", "get", "Name,Manufacturer,Model,Username"],
        "Boot Configuration": ["bootconfig", "get", "BootDirectory,ConfigurationPath"],
        "Time Zone": ["timezone", "get", "Caption,Bias"],
    },

    "Hardware": {
        "CPU Info": ["cpu", "get", "Name,NumberOfCores,MaxClockSpeed"],
        "BIOS Info": ["bios", "get", "Manufacturer,SMBIOSBIOSVersion"],
        "Baseboard (Motherboard)": ["baseboard", "get", "Manufacturer,Product,SerialNumber"],
        "Memory Modules": ["memorychip", "get", "Capacity,Speed,Manufacturer"],
    },

    "Storage": {
        "Disk Drives": ["diskdrive", "get", "Model,Size,InterfaceType"],
        "Logical Disks": ["logicaldisk", "get", "Name,FileSystem,FreeSpace,Size"],
        "Partitions": ["partition", "get", "Name,Size,Bootable"],
    },

    "Network": {
        "Network Adapters": ["nic", "where", "NetEnabled=true", "get", "Name,MACAddress"],
        "IP Configuration": ["nicconfig", "where", "IPEnabled=true", "get", "IPAddress,DefaultIPGateway"],
    },

    "Users & Sessions": {
        "Local User Accounts": ["useraccount", "get", "Name,Disabled,Lockout"],
        "Groups": ["group", "get", "Name"],
        "Logon Sessions": ["logonsession", "get", "LogonId,StartTime"],
    },

    "Software": {
        "Installed Products (Slow)": ["product", "get", "Name,Version"],
        "Services": ["service", "get", "Name,State,StartMode"],
        "Startup Programs": ["startup", "get", "Name,Command"],
    }
}

SAFE_DRIVERQUERY_COMMANDS = {
    "Basic": {
        "Loaded Drivers (Table)": ["driverquery"],
        "Loaded Drivers (No Header)": ["driverquery", "/NH"],
    },

    "Detailed": {
        "Verbose Driver Info": ["driverquery", "/V"],
        "Verbose (No Header)": ["driverquery", "/V", "/NH"],
    },

    "Security": {
        "Signed Drivers (CSV)": ["driverquery", "/FO", "CSV", "/SI"],
        "Signed Drivers (Table)": ["driverquery", "/SI"],
    },

    "Formats": {
        "Driver List (CSV)": ["driverquery", "/FO", "CSV"],
        "Driver List (LIST)": ["driverquery", "/FO", "LIST"],
    }
}

SAFE_IPCONFIG_COMMANDS = {
    "IP Summary": ["ipconfig"],
    "IP Full Details": ["ipconfig", "/all"],
    "DNS Cache": ["ipconfig", "/displaydns"],
    "DHCP Class ID (IPv4)": ["ipconfig", "/showclassid"],
    "DHCP Class ID (IPv6)": ["ipconfig", "/showclassid6"],
    "All Compartments": ["ipconfig", "/allcompartments"],
    "All Compartments (Full)": ["ipconfig", "/allcompartments", "/all"],
}

SAFE_PING_COMMANDS = {
    "Ping Host": {
        "cmd": ["ping", "-n", "4"],
        "input": True,
    },
    "Ping (Resolve Name)": {
        "cmd": ["ping", "-a", "-n", "4"],
        "input": True,
    },
    "Ping IPv4": {
        "cmd": ["ping", "-4", "-n", "4"],
        "input": True,
    },
    "Ping IPv6": {
        "cmd": ["ping", "-6", "-n", "4"],
        "input": True,
    },
    "Ping with Timeout": {
        "cmd": ["ping", "-n", "4", "-w", "1000"],
        "input": True,
    },
    "Ping MTU Test": {
        "cmd": ["ping", "-f", "-l", "1472", "-n", "2"],
        "input": True,
    },
    "Ping with TTL": {
        "cmd": ["ping", "-i", "64", "-n", "4"],
        "input": True,
    },
}

SAFE_TRACERT_COMMANDS = {
    "Trace Route": {
        "cmd": ["tracert"],
        "input": True,
    },
    "Trace Route (No DNS)": {
        "cmd": ["tracert", "-d"],
        "input": True,
    },
    "Trace Route IPv4": {
        "cmd": ["tracert", "-4"],
        "input": True,
    },
    "Trace Route IPv6": {
        "cmd": ["tracert", "-6"],
        "input": True,
    },
}

SAFE_NETSTAT_COMMANDS = {
    "Active Connections": ["netstat", "-a"],
    "Numerical Addresses": ["netstat", "-n"],
    "Connections + PID": ["netstat", "-o"],
    "Routing Table": ["netstat", "-r"],
    "Protocol Statistics": ["netstat", "-s"],
}

SAFE_SC_COMMANDS = {
    "List Running Services": {
        "cmd": ["sc", "query"],
        "input": False,
    },
    "List All Services": {
        "cmd": ["sc", "query", "state=", "all"],
        "input": False,
    },
    "Service Configuration": {
        "cmd": ["sc", "qc"],
        "input": True,
    },
    "Service Description": {
        "cmd": ["sc", "qdescription"],
        "input": True,
    },
    "Service Privileges": {
        "cmd": ["sc", "qprivs"],
        "input": True,
    },
    "Service Triggers": {
        "cmd": ["sc", "qtriggerinfo"],
        "input": True,
    },
}

SAFE_SCHTASKS_COMMANDS = {
    "List Tasks": {
        "cmd": ["schtasks", "/query"],
        "input": False,
    },
    "List Tasks (Verbose)": {
        "cmd": ["schtasks", "/query", "/v"],
        "input": False,
    },
    "List Tasks (Table)": {
        "cmd": ["schtasks", "/query", "/fo", "table", "/nh", "/v"],
        "input": False,
    },
    "Show Task SID": {
        "cmd": ["schtasks", "/ShowSid", "/TN"],
        "input": True,
    },
}

SAFE_ARP_COMMANDS = {
    "Show ARP Table": {
        "cmd": ["arp", "-a"],
        "input": False
    },
    "Show ARP Entry (IP)": {
        "cmd": ["arp", "-a"],
        "input": True
    },
    "Show ARP (Verbose)": {
        "cmd": ["arp", "-v"],
        "input": False
    },
    "Show ARP for Interface": {
        "cmd": ["arp", "-a", "-N"],
        "input": True
    }
}

SAFE_ROUTE_COMMANDS = {
    "Show Routing Table": {
        "cmd": ["route", "PRINT"],
        "input": False
    },
    "Show IPv4 Routes": {
        "cmd": ["route", "PRINT", "-4"],
        "input": False
    },
    "Show IPv6 Routes": {
        "cmd": ["route", "PRINT", "-6"],
        "input": False
    },
    "Filter Routes (Pattern)": {
        "cmd": ["route", "PRINT"],
        "input": True
    }
}

SAFE_NSLOOKUP_COMMANDS = {
    "Lookup Host (A Record)": {
        "cmd": ["nslookup"],
        "input": True
    },
    "Lookup MX Records": {
        "cmd": ["nslookup", "-type=MX"],
        "input": True
    },
    "Lookup NS Records": {
        "cmd": ["nslookup", "-type=NS"],
        "input": True
    },
    "Lookup Host Using Custom DNS": {
        "cmd": ["nslookup"],
        "input": True
    }
}

SAFE_NBTSTAT_COMMANDS = {
    "NetBIOS Cache": {
        "cmd": ["nbtstat", "-c"],
        "input": False
    },
    "Local NetBIOS Names": {
        "cmd": ["nbtstat", "-n"],
        "input": False
    },
    "Name Resolution Stats": {
        "cmd": ["nbtstat", "-r"],
        "input": False
    },
    "Active Sessions (IP)": {
        "cmd": ["nbtstat", "-S"],
        "input": False
    },
    "Remote Status (By Name)": {
        "cmd": ["nbtstat", "-a"],
        "input": True
    },
    "Remote Status (By IP)": {
        "cmd": ["nbtstat", "-A"],
        "input": True
    }
}

SAFE_PATHPING_COMMANDS = {
    "PathPing (Default)": {
        "cmd": ["pathping"],
        "input": True
    },
    "PathPing (No DNS)": {
        "cmd": ["pathping", "-n"],
        "input": True
    },
    "PathPing IPv4": {
        "cmd": ["pathping", "-4", "-n"],
        "input": True
    },
    "PathPing IPv6": {
        "cmd": ["pathping", "-6", "-n"],
        "input": True
    }
}

SAFE_NET_USER_COMMANDS = {
    "List Users": {
        "cmd": ["net", "user"],
        "input": False
    },
    "User Details": {
        "cmd": ["net", "user"],
        "input": True
    },
    "Domain User Details": {
        "cmd": ["net", "user"],
        "input": True,
        "extra": ["/domain"]
    }
}

SAFE_NET_LOCALGROUP_COMMANDS = {
    "List Local Groups": {
        "cmd": ["net", "localgroup"],
        "input": False
    },
    "View Local Group Members": {
        "cmd": ["net", "localgroup"],
        "input": True
    },
    "View Domain Group Members": {
        "cmd": ["net", "localgroup"],
        "input": True,
        "extra": ["/domain"]
    }
}

SAFE_NET_ACCOUNTS_COMMANDS = {
    "View Local Account Policy": {
        "cmd": ["net", "accounts"],
        "input": False
    },
    "View Domain Account Policy": {
        "cmd": ["net", "accounts"],
        "input": False,
        "extra": ["/domain"]
    }
}

SAFE_RUNAS_COMMANDS = {
    "Show Trust Levels": {
        "cmd": ["runas", "/showtrustlevels"],
        "input": False
    }
}

SAFE_GPUPDATE_COMMANDS = {
    "Update User and Computer Policy": {
        "cmd": ["gpupdate"],
        "input": False
    },
    "Update User Policy Only": {
        "cmd": ["gpupdate"],
        "input": False,
        "extra": ["/target:user"]
    },
    "Update Computer Policy Only": {
        "cmd": ["gpupdate"],
        "input": False,
        "extra": ["/target:computer"]
    },
    "Force Policy Refresh": {
        "cmd": ["gpupdate"],
        "input": False,
        "extra": ["/force"]
    }
}

SAFE_MOUNTVOL_COMMANDS = {
    "List All Volumes": {
        "cmd": ["mountvol"],
        "input": False
    },
    "List Volume for Path": {
        "cmd": ["mountvol"],
        "input": True,
        "extra": ["/L"]
    }
}

SAFE_DEFRAG_COMMANDS = {
    "Analyze Volume": {
        "cmd": ["defrag"],
        "input": True,
        "extra": ["/A", "/U", "/V"]
    },
    "Optimize Volume (Auto)": {
        "cmd": ["defrag"],
        "input": True,
        "extra": ["/O", "/U"]
    },
    "Retrim SSD": {
        "cmd": ["defrag"],
        "input": True,
        "extra": ["/L", "/U"]
    }
}

SAFE_BCDEDIT_COMMANDS = {
    "List Active Boot Entries": {
        "cmd": ["bcdedit"],
        "input": False
    },
    "List All Boot Entries": {
        "cmd": ["bcdedit"],
        "input": False,
        "extra": ["/enum", "all"]
    },
    "List Boot Entries (Verbose)": {
        "cmd": ["bcdedit"],
        "input": False,
        "extra": ["/enum", "/v"]
    }
}

SAFE_WEVTUTIL_COMMANDS = {
    "List Event Logs": {
        "cmd": ["wevtutil", "el"],
        "input": False
    },
    "List Event Publishers": {
        "cmd": ["wevtutil", "ep"],
        "input": False
    },
    "Get Log Configuration": {
        "cmd": ["wevtutil", "gl"],
        "input": True
    },
    "Get Log Status": {
        "cmd": ["wevtutil", "gli"],
        "input": True
    },
    "Query Recent Events": {
        "cmd": ["wevtutil", "qe"],
        "input": True,
        "extra": ["/c:20", "/f:text"]
    }
}

SAFE_AUDITPOL_COMMANDS = {
    "View Audit Policy": {
        "cmd": ["auditpol", "/get"],
        "input": False
    },
    "List Audit Categories": {
        "cmd": ["auditpol", "/list"],
        "input": False
    },
    "Backup Audit Policy": {
        "cmd": ["auditpol", "/backup"],
        "input": True
    }
}

SAFE_CIPHER_COMMANDS = {
    "Show Directory Encryption Status": {
        "cmd": ["cipher"],
        "input": False
    },
    "View File Encryption Info": {
        "cmd": ["cipher", "/C"],
        "input": True
    },
    "Show EFS Certificate Thumbprint": {
        "cmd": ["cipher", "/Y"],
        "input": False
    },
    "List Encrypted Files (No Key Update)": {
        "cmd": ["cipher", "/U", "/N"],
        "input": False
    }
}

SAFE_PNPUTIL_COMMANDS = {
    "Show PNPUTIL Help": {
        "cmd": ["pnputil", "/?"],
        "input": False
    },
    "List All Third-Party Drivers": {
        "cmd": ["pnputil", "/enum-drivers"],
        "input": False
    },
    "List All Devices (All States)": {
        "cmd": ["pnputil", "/enum-devices"],
        "input": False
    },
    "List Connected Devices Only": {
        "cmd": ["pnputil", "/enum-devices", "/connected"],
        "input": False
    },
    "List Disconnected Devices Only": {
        "cmd": ["pnputil", "/enum-devices", "/disconnected"],
        "input": False
    },
    "List Devices by Class": {
        "cmd": ["pnputil", "/enum-devices", "/class", "<ClassName|GUID>"],
        "input": True
    },
    "List Devices With Problems": {
        "cmd": ["pnputil", "/enum-devices", "/problem"],
        "input": False
    },
    "List Devices With Specific Problem Code": {
        "cmd": ["pnputil", "/enum-devices", "/problem", "<Code>"],
        "input": True
    },
    "List Device Hardware & Compatible IDs": {
        "cmd": ["pnputil", "/enum-devices", "/ids"],
        "input": False
    },
    "List Device Parent/Child Relationships": {
        "cmd": ["pnputil", "/enum-devices", "/relations"],
        "input": False
    },
    "List Device Driver Info": {
        "cmd": ["pnputil", "/enum-devices", "/drivers"],
        "input": False
    },
    "List All Device Interfaces": {
        "cmd": ["pnputil", "/enum-interfaces"],
        "input": False
    },
    "List Enabled Device Interfaces": {
        "cmd": ["pnputil", "/enum-interfaces", "/enabled"],
        "input": False
    },
    "List Disabled Device Interfaces": {
        "cmd": ["pnputil", "/enum-interfaces", "/disabled"],
        "input": False
    },
    "Scan for Hardware Changes": {
        "cmd": ["pnputil", "/scan-devices"],
        "input": False
    }
}
