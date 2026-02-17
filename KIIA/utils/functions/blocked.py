blocked_comm = {
    # Disk destruction
    "diskpart",
    "format",

    # Filesystem corruption
    "fsutil",

    # Boot / startup
    "bcdedit",

    # Registry (interactive & scripted)
    "regedit",

    # Scripting / shell escape
    "powershell",
    "cmd",

    # Shadow copies & recovery
    "vssadmin",

    # Low-level counters
    "lodctr",
}

admin_conf = {
    # File & directory modification
    "deld",
    "erase",
    "rmdir",

    # Disk & storage (non-destructive operations)
    "chkdsk",
    "defrag",
    "cipher",
    "mountvol",
    "vol",

    # System repair
    "sfc",
    "dism",

    # Users & security
    "net",
    "runas",
    "gpupdate",

    # Processes & services
    "taskkill",
    "sc",
    "services.msc",

    # Power & session control
    "shutdown",
    "logoff",
    "powercfg",

    # Scheduled tasks
    "schtasks",

    # Network modification
    "route",
    "arp",

    # Logs & auditing
    "wevtutil",
    "auditpol",

    # Hardware & drivers
    "pnputil",
    "devmgmt.msc",

    # Monitoring / system tools
    "perfmon",
    "resmon",
}
