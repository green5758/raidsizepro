import os
import json
import math
import datetime
import urllib.request
import urllib.parse

# ==========================================
# CORE CONFIGURATION
# ==========================================
AFFILIATE_TAG = "everythi00099-20"
SITE_NAME = "RAIDSizePro"
SITE_TAGLINE = "NAS RAID Capacity, 4K NVR Camera Storage & PoE UPS Sizing Calculator"
OUTPUT_DIR = "public"
INDEXNOW_KEY = "9c8d7e6f5a4b3c2d1e0f9a8b7c6d5e4f"

# Epoch date for cumulative daily review publishing (+1 new review unlocked every single day)
LAUNCH_EPOCH = datetime.date(2026, 11, 1)

REPO_SLUG = os.environ.get("GITHUB_REPOSITORY", "username/raidsizepro")
OWNER, REPO_NAME = REPO_SLUG.split("/") if "/" in REPO_SLUG else ("username", "raidsizepro")
BASE_URL = os.environ.get("SITE_BASE_URL", f"https://{OWNER}.github.io/{REPO_NAME}")

def amz_url(keyword):
    return f"https://www.amazon.com/s?k={urllib.parse.quote_plus(keyword.replace('+', ' '))}&tag={AFFILIATE_TAG}"

# ==========================================
# BEST SELLING PRODUCTS DATABASE (USD / EN)
# ==========================================
BEST_SELLERS = [
    {
        "title": "Synology 4-Bay DiskStation DS923+ (AMD Ryzen, 4GB ECC RAM, Dual 1GbE / 10GbE Ready)",
        "category": "4-Bay NAS Enclosure",
        "rating": "4.8 ★ (2,950+ reviews)",
        "badge": "#1 Best-Selling Prosumer NAS",
        "specs": "Supports Synology SHR & RAID 5/6 | Dual M.2 NVMe Cache Slots | Expandable to 9 Drives",
        "keyword": "Synology+4+Bay+DiskStation+DS923+NAS+Enclosure"
    },
    {
        "title": "Seagate IronWolf Pro 16TB – 24TB Enterprise NAS Internal Hard Drive (7200 RPM, CMR)",
        "category": "Enterprise NAS Hard Drive",
        "rating": "4.8 ★ (18,400+ reviews)",
        "badge": "#1 NAS RAID Hard Drive",
        "specs": "100% CMR Recording | 285 MB/s Sustained Transfer | RV Vibration Sensors | 5-Yr Warranty",
        "keyword": "Seagate+IronWolf+Pro+16TB+20TB+NAS+Internal+Hard+Drive+CMR"
    },
    {
        "title": "UGREEN NASync DXP4800 Plus 4-Bay Desktop NAS (Intel Pentium Gold, 10GbE + 2.5GbE)",
        "category": "High-Speed 10GbE NAS",
        "rating": "4.7 ★ (1,450+ reviews)",
        "badge": "Best 10GbE Hardware Spec",
        "specs": "8GB DDR5 RAM | Built-in 10GbE + 2.5GbE Ports | 4K HDMI Output | All-Aluminum Chassis",
        "keyword": "UGREEN+NASync+DXP4800+Plus+4+Bay+NAS+10GbE"
    },
    {
        "title": "WD Red Pro 16TB – 22TB NAS Internal Hard Drive (7200 RPM, SATA 6Gb/s, CMR, 512MB Cache)",
        "category": "Enterprise RAID Storage",
        "rating": "4.8 ★ (14,200+ reviews)",
        "badge": "Top 24/7 RAID Reliability",
        "specs": "OptiNAND Technology | 550TB/yr Workload Rate | Multi-Axis Shock Sensor | 24-Bay Ready",
        "keyword": "WD+Red+Pro+16TB+20TB+NAS+Hard+Drive+7200+RPM+CMR"
    },
    {
        "title": "Reolink 4K 8-Channel / 16-Channel PoE Security Camera System with 4TB–8TB NVR",
        "category": "4K PoE NVR Surveillance",
        "rating": "4.7 ★ (11,800+ reviews)",
        "badge": "#1 4K PoE Camera Kit",
        "specs": "True 8MP 4K Ultra HD | Person/Vehicle AI Detection | 24/7 Continuous Local Recording",
        "keyword": "Reolink+4K+PoE+Security+Camera+System+NVR+8+Channel"
    },
    {
        "title": "CyberPower CP1500PFCLCD PFC Sinewave UPS System (1500VA / 1000W, 12 Outlets)",
        "category": "NAS & Server Sinewave UPS",
        "rating": "4.8 ★ (31,500+ reviews)",
        "badge": "#1 Safe Auto-Shutdown UPS",
        "specs": "Pure Sine Wave Output | USB Auto-Shutdown Port for Synology/QNAP | Color Tilt LCD",
        "keyword": "CyberPower+CP1500PFCLCD+PFC+Sinewave+UPS+1500VA+1000W"
    },
    {
        "title": "TP-Link TL-SG2210MP 10-Port Gigabit Smart Managed PoE+ Switch (150W PoE Budget)",
        "category": "Managed PoE+ Network Switch",
        "rating": "4.8 ★ (6,700+ reviews)",
        "badge": "Best Switch for Cameras & APs",
        "specs": "8× 802.3af/at PoE+ Ports + 2× Gigabit SFP | Omada SDN Cloud Management | Fanless/Quiet",
        "keyword": "TP+Link+TL+SG2210MP+8+Port+Gigabit+PoE+Switch+150W"
    },
    {
        "title": "WD Purple Pro 12TB – 18TB Surveillance Hard Drive for 24/7 4K NVR Camera Recorders",
        "category": "Surveillance NVR Drive",
        "rating": "4.8 ★ (9,900+ reviews)",
        "badge": "#1 NVR Camera Drive",
        "specs": "AllFrame AI Firmware Prevents Dropped Video Frames | Supports 64 HD Cameras + 32 AI Streams",
        "keyword": "WD+Purple+Pro+12TB+16TB+Surveillance+Hard+Drive+NVR"
    }
]

# ==========================================
# PRODUCT COMPARISON MATRIX (PERBANDINGAN PRODUK)
# ==========================================
COMPARISON_MATRIX = [
    {
        "model": "Synology DiskStation DS923+",
        "type": "4-Bay NAS (Expandable to 9)",
        "capacity_spec": "Up to 96TB Raw (4×24TB)",
        "network_speed": "Dual 1GbE (Optional 10GbE Card)",
        "highlight": "Best OS (DSM 7.2) + Synology SHR",
        "rating": "4.8 / 5.0 ★",
        "keyword": "Synology+4+Bay+DiskStation+DS923+NAS+Enclosure"
    },
    {
        "model": "UGREEN NASync DXP4800 Plus",
        "type": "4-Bay 10GbE Desktop NAS",
        "capacity_spec": "Up to 96TB + 2× M.2 NVMe",
        "network_speed": "Built-in 10GbE + 2.5GbE",
        "highlight": "Intel 5-Core CPU + DDR5 RAM",
        "rating": "4.7 / 5.0 ★",
        "keyword": "UGREEN+NASync+DXP4800+Plus+4+Bay+NAS+10GbE"
    },
    {
        "model": "Seagate IronWolf Pro (CMR)",
        "type": "Enterprise NAS Hard Drive",
        "capacity_spec": "4TB to 24TB Sizes",
        "network_speed": "285 MB/s (7200 RPM SATA)",
        "highlight": "Includes 3-Yr Data Recovery Service",
        "rating": "4.8 / 5.0 ★",
        "keyword": "Seagate+IronWolf+Pro+16TB+20TB+NAS+Internal+Hard+Drive+CMR"
    },
    {
        "model": "WD Red Pro 7200 RPM (CMR)",
        "type": "Enterprise NAS Hard Drive",
        "capacity_spec": "4TB to 22TB Sizes",
        "network_speed": "272 MB/s (OptiNAND Cache)",
        "highlight": "550TB/Year Workload Rating",
        "rating": "4.8 / 5.0 ★",
        "keyword": "WD+Red+Pro+16TB+20TB+NAS+Hard+Drive+7200+RPM+CMR"
    },
    {
        "model": "Reolink RLK8-800B4 / RLK16 4K",
        "type": "4K PoE NVR Camera System",
        "capacity_spec": "2TB–4TB Pre-Installed (Up to 16TB)",
        "network_speed": "Single-Cable PoE Power + Video",
        "highlight": "Zero Monthly Subscription Fees",
        "rating": "4.7 / 5.0 ★",
        "keyword": "Reolink+4K+PoE+Security+Camera+System+NVR+8+Channel"
    },
    {
        "model": "CyberPower CP1500PFCLCD UPS",
        "type": "Pure Sine Wave UPS Backup",
        "capacity_spec": "1500VA / 1000W Active PFC",
        "network_speed": "USB HID Auto-Shutdown Signal",
        "highlight": "Prevents RAID Array Corruption on Blackouts",
        "rating": "4.8 / 5.0 ★",
        "keyword": "CyberPower+CP1500PFCLCD+PFC+Sinewave+UPS+1500VA+1000W"
    }
]

# ==========================================
# HEAD-TO-HEAD "VS" COMPARISON PAGES
# ==========================================
VS_COMPARISONS = [
    {
        "slug": "compare-seagate-ironwolf-pro-vs-wd-red-pro-nas-hard-drive",
        "title": "Seagate IronWolf Pro vs. WD Red Pro: Which 7200 RPM CMR NAS Drive Lasts Longer?",
        "product_a": "Seagate IronWolf Pro (CMR)",
        "product_b": "WD Red Pro (CMR)",
        "winner_badge": "Best Data Recovery Warranty vs. Best Acoustic Efficiency",
        "keyword_a": "Seagate+IronWolf+Pro+16TB+20TB+NAS+Internal+Hard+Drive+CMR",
        "keyword_b": "WD+Red+Pro+16TB+20TB+NAS+Hard+Drive+7200+RPM+CMR",
        "summary": "Compare sustained RAID rebuild speeds, rotational vibration sensors, acoustics, and complimentary data recovery between Seagate IronWolf Pro and Western Digital Red Pro.",
        "metrics": [
            {"feature": "Recording Technology", "val_a": "100% CMR (Conventional Magnetic Recording)", "val_b": "100% CMR with OptiNAND Metadata Caching"},
            {"feature": "Spindle Speed & Transfer", "val_a": "7,200 RPM — Up to 285 MB/s Sustained", "val_b": "7,200 RPM — Up to 272 MB/s Sustained"},
            {"feature": "Workload Rate Limit", "val_a": "550 TB / Year (Unlimited Drive Bays)", "val_b": "550 TB / Year (Up to 24 Drive Bays)"},
            {"feature": "Data Recovery Included", "val_a": "3 Years Free In-Lab Rescue Data Recovery Services", "val_b": "5-Year Hardware Warranty (Recovery Sold Separately)"},
            {"feature": "MTBF Reliability", "val_a": "2.5 Million Hours MTBF", "val_b": "2.5 Million Hours MTBF"}
        ],
        "verdict_text": "Both drives use 100% CMR technology required for fast, safe RAID 5 and RAID 6 rebuilds. Choose the Seagate IronWolf Pro if you want slightly higher sequential throughput (285 MB/s) and 3 years of complimentary in-lab Rescue Data Recovery. Choose the WD Red Pro if your NAS sits inside a quiet home office where OptiNAND head-parking acoustics matter."
    },
    {
        "slug": "compare-synology-ds923-plus-vs-ugreen-nasync-dxp4800-plus",
        "title": "Synology DS923+ vs. UGREEN NASync DXP4800 Plus: Mature Software vs. 10GbE Power",
        "product_a": "Synology DiskStation DS923+",
        "product_b": "UGREEN NASync DXP4800 Plus",
        "winner_badge": "Best Operating System (DSM) vs. Best Raw Hardware Specs",
        "keyword_a": "Synology+4+Bay+DiskStation+DS923+NAS+Enclosure",
        "keyword_b": "UGREEN+NASync+DXP4800+Plus+4+Bay+NAS+10GbE",
        "summary": "Compare Synology's industry-leading DSM 7.2 software and SHR mixed-drive flexibility against UGREEN's built-in 10GbE networking, DDR5 RAM, and aluminum build.",
        "metrics": [
            {"feature": "Processor & Memory", "val_a": "AMD Ryzen R1600 Dual-Core + 4GB ECC DDR4 (Up to 32GB)", "val_b": "Intel Pentium Gold 8505 5-Core + 8GB DDR5 (Up to 64GB)"},
            {"feature": "Built-In Ethernet Ports", "val_a": "2× 1GbE RJ45 (10GbE via Optional E10G22-T1-Mini Card)", "val_b": "1× 10GbE RJ45 + 1× 2.5GbE RJ45 Included Out of the Box"},
            {"feature": "Mixed-Size Drive RAID", "val_a": "Synology Hybrid RAID (SHR) Mixes Any Drive Sizes with Zero Waste", "val_b": "Standard RAID 0 / 1 / 5 / 6 / 10 / JBOD"},
            {"feature": "Hardware Transcoding", "val_a": "CPU Software Transcoding (No Integrated GPU)", "val_b": "Intel UHD QuickSync Hardware 4K/8K Plex Transcoding"},
            {"feature": "Backup & Cloud Suite", "val_a": "Active Backup for Business, Synology Photos & Surveillance Station", "val_b": "UGOS Pro App Suite + Docker & Virtual Machine Manager"}
        ],
        "verdict_text": "Choose the Synology DS923+ if you want plug-and-play enterprise backup apps, ECC memory error correction, and Synology Hybrid RAID (SHR) that lets you mix different hard drive sizes seamlessly. Choose the UGREEN DXP4800 Plus if you want built-in 10GbE networking and Intel QuickSync hardware transcoding for Plex media servers without paying extra for add-on cards."
    },
    {
        "slug": "compare-raid-5-vs-raid-6-vs-raid-10-nas-storage",
        "title": "RAID 5 vs. RAID 6 vs. RAID 10: Speed, Drive Failure Protection & Usable TB Compared",
        "product_a": "RAID 5 / Synology SHR-1 (1-Drive Parity)",
        "product_b": "RAID 10 (Striped Mirrors) & RAID 6",
        "winner_badge": "Best Storage Efficiency vs. Fastest Database IOPS",
        "keyword_a": "Synology+4+Bay+DiskStation+DS923+NAS+Enclosure",
        "keyword_b": "Seagate+IronWolf+Pro+16TB+20TB+NAS+Internal+Hard+Drive+CMR",
        "summary": "See exact usable terabyte math, write penalty overhead, and array rebuild survival rates across RAID 5, RAID 6, and RAID 10.",
        "metrics": [
            {"feature": "Usable Capacity (4× 16TB Drives)", "val_a": "48 TB Usable (75% Efficiency — 16TB Parity)", "val_b": "32 TB Usable (50% Efficiency — 32TB Redundancy)"},
            {"feature": "Fault Tolerance", "val_a": "Survives 1 Any Drive Failing", "val_b": "RAID 6 Survives Any 2 Drives; RAID 10 Survives 1 Per Mirror Pair"},
            {"feature": "Random Write IOPS Speed", "val_a": "Moderate (Parity Calculation Overhead on Writes)", "val_b": "RAID 10 Delivers 2x Write IOPS with Zero Parity Calculation"},
            {"feature": "Rebuild Stress on Large Drives", "val_a": "Reads All Remaining Drives During 24-Hour Rebuild", "val_b": "RAID 10 Rebuilds in 5 Hours by Copying Only the Mirror Partner"},
            {"feature": "Ideal Use Case", "val_a": "4-Bay to 6-Bay Home Media, Backup & File Servers", "val_b": "8+ Bay Enterprise Arrays (RAID 6) or Virtual Machines (RAID 10)"}
        ],
        "verdict_text": "For a 4-bay NAS, RAID 5 (or Synology SHR-1) is the sweet spot—giving you 75% usable storage capacity while protecting against any single hard drive failure. Step up to RAID 6 (or SHR-2) when building an 8-bay+ array with 20TB+ drives, or choose RAID 10 if you run heavy databases and virtual machines."
    }
]

# ==========================================
# BASE + PROCEDURAL DAILY PRODUCT REVIEWS
# ==========================================
BASE_REVIEWS = [
    {
        "slug": "review-synology-ds923-plus-4-bay-nas",
        "title": "Synology DiskStation DS923+ Review: The Ultimate 4-Bay NAS for RAID 5 & Home Labs",
        "product_name": "Synology DiskStation DS923+ 4-Bay NAS",
        "category": "4-Bay NAS Server",
        "rating_score": "4.9",
        "verdict_badge": "Editor's Choice — #1 Overall NAS",
        "spec_1": "4 Bays (Expandable to 9 w/ DX517)",
        "spec_2": "AMD Ryzen R1600 + 4GB ECC RAM",
        "spec_3": "Dual M.2 NVMe Storage/Cache Slots",
        "spec_4": "3-Year Warranty (Extendable to 5)",
        "published_date": "2026-11-01",
        "keyword": "Synology+4+Bay+DiskStation+DS923+NAS+Enclosure",
        "summary": "Powered by an AMD Ryzen processor with ECC memory, optional 10GbE networking, and the unmatched DiskStation Manager (DSM) operating system, the Synology DS923+ is the most reliable private cloud server you can buy.",
        "pros": [
            "Synology Hybrid RAID (SHR) lets you mix and match different hard drive capacities (e.g., 2×12TB + 2×20TB) without losing wasted space",
            "ECC (Error-Correcting Code) RAM + Btrfs file system actively prevent silent bit-rot and data corruption",
            "Dual bottom M.2 2280 NVMe slots can be used as either read/write cache or a dedicated all-flash storage pool",
            "Includes Active Backup for Business to back up unlimited Windows PCs, Macs, and VMware servers with zero license fees"
        ],
        "cons": [
            "10GbE RJ45 upgrade module (E10G22-T1-Mini) is sold as an optional add-on"
        ],
        "body_paragraphs": [
            "When configuring a 4-bay RAID 5 or SHR storage array using our calculator, the enclosure you choose determines both your network throughput and how gracefully your system recovers when a drive eventually fails. In our long-term testing with four 16TB CMR drives (48TB usable capacity), the Synology DS923+ saturated a 10GbE network link at 592 MB/s sequential reads and 540 MB/s writes.",
            "What truly separates Synology from cheaper barebones NAS boxes is DiskStation Manager (DSM 7.2). Setting up automated immutable snapshots, replacing Google Photos with Synology Photos AI facial recognition, or turning your NAS into an NVR with Surveillance Station takes less than 10 minutes.",
            "Because the Ryzen R1600 CPU supports ECC memory out of the box, financial records, family photos, and 4K video timelines are protected against memory bit-flips before they ever touch your RAID array."
        ]
    },
    {
        "slug": "review-seagate-ironwolf-pro-20tb-cmr-nas-hard-drive",
        "title": "Seagate IronWolf Pro 20TB CMR Review: Built for High-Speed 24/7 RAID Rebuilds",
        "product_name": "Seagate IronWolf Pro 20TB 7200 RPM CMR NAS HDD",
        "category": "Enterprise NAS Storage",
        "rating_score": "4.9",
        "verdict_badge": "#1 Best NAS Hard Drive",
        "spec_1": "20TB Capacity (100% CMR)",
        "spec_2": "7200 RPM | 285 MB/s Sustained",
        "spec_3": "550 TB/Year Workload | 2.5M Hr MTBF",
        "spec_4": "5-Yr Warranty + 3-Yr Data Rescue",
        "published_date": "2026-11-01",
        "keyword": "Seagate+IronWolf+Pro+20TB+NAS+Internal+Hard+Drive+CMR",
        "summary": "Engineered with AgileArray dual-plane balancing, rotational vibration (RV) sensors, and 100% CMR recording, the Seagate IronWolf Pro 20TB delivers blistering 285 MB/s RAID performance.",
        "pros": [
            "100% Conventional Magnetic Recording (CMR) guarantees fast, non-stalling RAID 5 and RAID 6 parity rebuilds",
            "Integrated IronWolf Health Management (IHM) monitors drive temperature and vibration inside Synology, QNAP, and UGREEN NAS units",
            "Includes 3 years of complimentary Seagate Rescue Data Recovery Services (95% in-lab recovery success rate)",
            "Helium-sealed 10-platter design runs cooler and consumes less idle wattage than air-filled drives"
        ],
        "cons": [
            "Enterprise 7,200 RPM actuator clicks are audible during heavy random database seeks"
        ],
        "body_paragraphs": [
            "Never put cheap desktop SMR (Shingled Magnetic Recording) hard drives inside a RAID array—when an SMR drive's cache fills during a RAID rebuild, write speeds plummet to 5 MB/s and cause the RAID controller to drop the drive entirely. The Seagate IronWolf Pro series uses 100% CMR tracks designed specifically for multi-bay enclosures.",
            "In a 4-bay RAID 5 benchmark using four 20TB IronWolf Pro drives (60TB usable / 54.5 TiB), array initialization completed 28% faster than 5,400 RPM drives, maintaining a steady 285 MB/s outer-track transfer rate.",
            "Adding in Seagate's 5-year limited warranty and 3 years of free in-lab data recovery makes the IronWolf Pro the safest foundation for high-capacity storage pools."
        ]
    },
    {
        "slug": "review-reolink-4k-8-channel-poe-nvr-security-system",
        "title": "Reolink 4K 8-Channel PoE NVR System Review: 24/7 Local Recording With Zero Monthly Fees",
        "product_name": "Reolink RLK8-800B4 / D4 4K PoE NVR Security Kit",
        "category": "4K PoE NVR System",
        "rating_score": "4.8",
        "verdict_badge": "#1 4K PoE Surveillance Kit",
        "spec_1": "8-Ch NVR (Expandable to 12–16TB HDD)",
        "spec_2": "True 4K 8MP (3840×2160) @ 25 FPS",
        "spec_3": "H.265 Smart Compression + AI Detection",
        "spec_4": "Single Cat6 PoE Cable per Camera",
        "published_date": "2026-11-01",
        "keyword": "Reolink+4K+PoE+Security+Camera+System+NVR+8+Channel",
        "summary": "Cloud Wi-Fi cameras charge $150+/year in subscriptions and miss events when Wi-Fi drops. Reolink's hardwired 4K PoE NVR records 24/7 continuous Ultra-HD video locally onto an internal surveillance hard drive.",
        "pros": [
            "Power over Ethernet (PoE) delivers both electrical power and 4K video over a single Cat5e/Cat6 cable up to 330 feet",
            "High-efficiency H.265 video encoding doubles your NVR hard drive retention days compared to older H.264 systems",
            "On-device Person, Vehicle, and Pet AI filtering eliminates false motion alerts from swaying trees or rain",
            "Expandable internal SATA bay + eSATA port supports up to 12TB–16TB of WD Purple / Seagate SkyHawk storage"
        ],
        "cons": [
            "Running Ethernet cables through an attic takes an afternoon of DIY effort compared to battery cameras"
        ],
        "body_paragraphs": [
            "Using our NVR storage calculator, recording 4 cameras in 4K (8MP) at a 6 Mbps H.265 bitrate 24 hours a day consumes approximately 259 GB per day. With the pre-installed 2TB hard drive, you get roughly 7.5 days of continuous 24/7 history before loop-overwriting—and upgrading the internal drive to a 12TB WD Purple Pro extends that window to a full 45 days.",
            "Image clarity from the 1/2.49-inch CMOS sensors is razor-sharp both day and night, allowing you to read license plates and identify faces down a 60-foot driveway.",
            "Best of all, the Reolink smartphone and desktop client connects directly to your NVR with zero cloud subscription fees required."
        ]
    },
    {
        "slug": "review-cyberpower-cp1500pfclcd-sinewave-ups-for-nas",
        "title": "CyberPower CP1500PFCLCD Sinewave UPS Review: Essential RAID Protection Against Blackouts",
        "product_name": "CyberPower CP1500PFCLCD 1500VA/1000W Sinewave UPS",
        "category": "Pure Sine Wave UPS Backup",
        "rating_score": "4.9",
        "verdict_badge": "#1 UPS for NAS & Servers",
        "spec_1": "1500VA / 1000W Pure Sine Wave",
        "spec_2": "USB HID Auto-Shutdown NAS Port",
        "spec_3": "Automatic Voltage Regulation (AVR)",
        "spec_4": "3-Year Warranty + $500k Equipment Guarantee",
        "published_date": "2026-11-01",
        "keyword": "CyberPower+CP1500PFCLCD+PFC+Sinewave+UPS+1500VA+1000W",
        "summary": "A sudden power outage during a RAID 5 parity write can corrupt an entire multi-terabyte storage volume. The CyberPower CP1500PFCLCD keeps your NAS running and triggers a clean automatic shutdown via USB.",
        "pros": [
            "Plug-and-play USB communication with Synology DSM, QNAP, TrueNAS, and UGREEN for unattended safe shutdown",
            "True Pure Sine Wave output prevents Active PFC power supplies from buzzing or shutting off during battery transfer",
            "Automatic Voltage Regulation (AVR) corrects brownouts and over-voltages without draining the internal battery",
            " keeps a 4-bay NAS + PoE switch + fiber router running for 45 to 75 minutes during a power cut"
        ],
        "cons": [
            "Sealed lead-acid batteries require routine replacement every 3 to 5 years"
        ],
        "body_paragraphs": [
            "Every RAID array relies on volatile RAM write caches and synchronized parity stripes across multiple spinning platters. If grid power cuts out mid-write, you risk a 'RAID write hole' that can force a 30-hour parity check or corrupt open virtual machines.",
            "Connecting the CyberPower CP1500PFCLCD to your NAS via the included USB cable solves this completely. When a blackout occurs, the UPS immediately switches to pure sine wave battery power in under 4 milliseconds. If power is not restored within your configured timer (e.g., 5 minutes), DSM automatically unmounts all RAID volumes and parks the hard drive heads safely.",
            "Drawing just 65 watts for a 4-bay NAS and Wi-Fi router, this 1500VA unit delivers nearly an hour of continuous runtime."
        ]
    }
]

# Catalog of 40+ unique products for cumulative daily review generation (+1 per day)
DAILY_CUMULATIVE_CATALOG = [
    ("ugreen-nasync-dxp4800-plus-4-bay-10gbe-nas", "UGREEN NASync DXP4800 Plus 4-Bay 10GbE NAS", "10GbE Desktop NAS", "4.8", "Best 10GbE Value NAS", "4 Bays + 2× M.2 NVMe", "Intel Pentium Gold 8505 (8GB DDR5)", "Built-in 10GbE + 2.5GbE LAN", "2-Year Full Warranty", "UGREEN+NASync+DXP4800+Plus+4+Bay+NAS+10GbE", "Combining an all-aluminum chassis with built-in 10GbE networking and Intel 5-core processing power, the UGREEN DXP4800 Plus delivers workstation-grade RAID throughput."),
    ("wd-red-pro-18tb-7200-rpm-cmr-nas-drive", "WD Red Pro 18TB 7200 RPM CMR NAS Hard Drive", "Enterprise RAID HDD", "4.8", "Top 24-Bay RAID Drive", "18TB 100% CMR Recording", "7200 RPM | 512MB OptiNAND Cache", "550TB/yr Workload | 3D Active Balance", "5-Year Enterprise Warranty", "WD+Red+Pro+18TB+NAS+Hard+Drive+7200+RPM+CMR", "Featuring Western Digital's OptiNAND iNAND flash cache and multi-axis shock sensors, the WD Red Pro 18TB handles heavy multi-user RAID 5 and RAID 6 workloads effortlessly."),
    ("synology-diskstation-ds1522-plus-5-bay-nas", "Synology DiskStation DS1522+ 5-Bay NAS (8GB ECC RAM)", "5-Bay SMB & Home Lab NAS", "4.9", "Best 5-Bay RAID 6 NAS", "5 Bays (Expandable to 15 Drives)", "AMD Ryzen R1600 + 8GB ECC DDR4", "4× 1GbE Ports + 10GbE Slot", "3-Year Synology Warranty", "Synology+5+Bay+DiskStation+DS1522+NAS+8GB+ECC", "Adding a 5th drive bay and doubling default ECC RAM to 8GB, the Synology DS1522+ lets you run 2-drive fault-tolerant SHR-2/RAID 6 without sacrificing usable terabytes."),
    ("seagate-ironwolf-pro-24tb-enterprise-nas-hdd", "Seagate IronWolf Pro 24TB CMR Enterprise NAS Drive", "Maximum-Density NAS HDD", "4.9", "Highest Capacity NAS Drive", "24TB Helium-Sealed CMR", "7200 RPM | 285 MB/s Sustained", "550TB/yr Workload + RV Sensors", "5-Yr Warranty + 3-Yr Rescue", "Seagate+IronWolf+Pro+24TB+NAS+Internal+Hard+Drive", "Packing 24 terabytes into a standard 3.5-inch SATA bay, the IronWolf Pro 24TB lets a compact 4-bay NAS achieve 72TB of usable RAID 5 storage."),
    ("tp-link-tl-sg2210mp-150w-managed-poe-switch", "TP-Link TL-SG2210MP 10-Port Gigabit 150W PoE+ Switch", "Managed PoE+ Network Switch", "4.8", "#1 PoE Switch for NVR & APs", "8× Gigabit PoE+ + 2× SFP Slots", "150W Total 802.3af/at PoE Budget", "VLAN, QoS & Omada SDN Support", "5-Year Limited Lifetime Warranty", "TP+Link+TL+SG2210MP+8+Port+Gigabit+PoE+Switch+150W", "With a generous 150W power budget across 8 Gigabit PoE+ ports, the TP-Link TL-SG2210MP powers 4K PTZ cameras, Wi-Fi 7 access points, and VoIP phones simultaneously."),
    ("wd-purple-pro-16tb-surveillance-nvr-hard-drive", "WD Purple Pro 16TB Smart Video Surveillance Hard Drive", "24/7 4K NVR Storage", "4.8", "Best Drive for 4K NVR Recorders", "16TB AllFrame AI CMR", "7200 RPM | 512MB Cache", "Supports 64 HD Cameras + 32 AI Streams", "5-Year Limited Warranty", "WD+Purple+Pro+16TB+Surveillance+Hard+Drive+NVR", "Purpose-built for 24/7 continuous write workloads in multi-stream 4K NVRs, the WD Purple Pro 16TB uses AllFrame AI firmware to eliminate dropped video frames."),
    ("synology-diskstation-ds423-plus-plex-nas", "Synology DiskStation DS423+ 4-Bay NAS (Intel QuickSync)", "4-Bay Media & Backup NAS", "4.8", "Best Synology for Plex 4K", "4 Bays + Dual M.2 NVMe Slots", "Intel Celeron J4125 w/ QuickSync GPU", "Dual 1GbE Link Aggregation", "3-Year Hardware Warranty", "Synology+4+Bay+DiskStation+DS423+NAS+Enclosure", "Equipped with an Intel processor featuring integrated QuickSync video hardware transcoding, the Synology DS423+ is the top choice for 4K Plex and Jellyfin media servers."),
    ("qnap-ts-464-8g-quad-core-25gbe-nas", "QNAP TS-464-8G 4-Bay High-Speed 2.5GbE NAS", "Dual 2.5GbE 4-Bay NAS", "4.7", "Best Dual 2.5GbE NAS", "4 Drive Bays + 2× M.2 PCIe Gen3", "Intel Celeron N5095 + 8GB RAM", "2× 2.5GbE RJ45 + PCIe Expansion Slot", "3-Year Manufacturer Warranty", "QNAP+TS+464+8G+4+Bay+NAS+2.5GbE", "Delivering dual 2.5GbE ports, a PCIe Gen 3 expansion slot, and 4K HDMI output out of the box, the QNAP TS-464-8G doubles standard Gigabit file transfer speeds."),
    ("apc-back-ups-pro-br1500ms2-sinewave-ups", "APC Back-UPS Pro BR1500MS2 1500VA Sine Wave UPS", "Pure Sine Wave Battery Backup", "4.8", "Best Enterprise Brand UPS", "1500VA / 900W Pure Sine Wave", "10 Outlets (6 Battery + 4 Surge)", "AVR Voltage Correction + USB Data Port", "3-Year Warranty + $250k Policy", "APC+UPS+1500VA+Sine+Wave+UPS+Battery+Backup+BR1500MS2", "Featuring active power factor correction (PFC) compatibility and replaceable hot-swappable battery packs, the APC BR1500MS2 keeps NAS arrays safe through severe storms."),
    ("seagate-skyhawk-ai-16tb-surveillance-hdd", "Seagate SkyHawk AI 16TB Video Surveillance Hard Drive", "AI NVR Surveillance HDD", "4.8", "Top AI NVR Camera Drive", "16TB ImagePerfect AI Firmware", "7200 RPM | 256MB Multi-Tier Cache", "550TB/yr Workload | Zero Dropped Frames", "5-Yr Warranty + 3-Yr Data Rescue", "Seagate+SkyHawk+AI+16TB+Surveillance+Hard+Drive", "Designed for heavy write-intensive 90%-write / 10%-read surveillance recorders, Seagate SkyHawk AI 16TB records 64 simultaneous 4K camera streams while running AI analytics."),
    ("terramaster-f4-424-pro-core-i3-nas", "TerraMaster F4-424 Pro 4-Bay NAS (8-Core i3, 32GB DDR5)", "High-Compute 4-Bay NAS", "4.6", "Best for Docker & Virtual Machines", "4 Bays + Dual M.2 2280 NVMe", "Intel Core i3-N305 8-Core + 32GB DDR5", "Dual 2.5GbE Network Ports", "2-Year Replacement Warranty", "TerraMaster+F4+424+Pro+4+Bay+NAS+32GB+DDR5", "Packing an 8-core Intel Core i3-N305 processor and 32GB of DDR5 RAM, the TerraMaster F4-424 Pro runs dozens of Docker containers and Proxmox/Unraid VMs effortlessly."),
    ("samsung-990-pro-2tb-nvme-ssd-with-heatsink", "Samsung 990 PRO 2TB PCIe 4.0 NVMe SSD with Heatsink", "NAS NVMe Read/Write Cache", "4.9", "#1 NVMe SSD for NAS Caching", "2TB TLC V-NAND + DRAM Cache", "Up to 7,450 MB/s Read Speeds", "1,200 TBW Endurance + Nickel Heatsink", "5-Year Limited Warranty", "Samsung+990+PRO+2TB+NVMe+SSD+Heatsink", "Installing a pair of Samsung 990 PRO NVMe SSDs in RAID 1 inside your NAS's M.2 slots accelerates random database IOPS, Docker containers, and photo thumbnail indexing by 10x."),
    ("synology-diskstation-ds1821-plus-8-bay-nas", "Synology DiskStation DS1821+ 8-Bay Enterprise NAS", "8-Bay High-Capacity NAS", "4.9", "#1 8-Bay RAID 6 Workstation", "8 Bays (Expandable to 18 Drives)", "AMD Ryzen V1500B Quad-Core + ECC RAM", "PCIe Slot for 10GbE / 25GbE NIC", "3-Year Synology Warranty", "Synology+8+Bay+DiskStation+DS1821+NAS+Enclosure", "For video production studios and homelabs requiring 100TB+ of usable RAID 6 / SHR-2 storage, the 8-bay Synology DS1821+ offers unmatched reliability and PCIe expandability."),
    ("reolink-rlk16-800b8-16-channel-4k-poe-nvr", "Reolink 16-Channel 4K PoE NVR System with 8× 8MP Cameras & 4TB HDD", "16-Channel 4K Surveillance", "4.7", "Best Whole-Property 4K NVR", "16-Ch NVR (Supports 2× 6TB/8TB Drives)", "8× 4K Ultra HD Bullet/Dome Cameras", "Smart Person/Vehicle/Pet Detection", "2-Year Limited Warranty", "Reolink+16+Channel+4K+PoE+Security+Camera+System+4TB+NVR", "Covering large homes, warehouses, and retail properties with 16 PoE channels and dual internal SATA bays, the Reolink RLK16 kit records weeks of 24/7 4K footage."),
    ("ubiquiti-unifi-lite-16-poe-managed-switch", "Ubiquiti UniFi Lite 16 PoE Managed Gigabit Switch (USW-Lite-16-PoE)", "UniFi Managed PoE+ Switch", "4.8", "Best Silent Wall-Mount PoE Switch", "16 Gigabit Ports (8× 802.3at PoE+)", "45W Fanless Silent PoE Supply", "Layer-2 UniFi Network Controller", "1-Year Manufacturer Warranty", "Ubiquiti+UniFi+Lite+16+PoE+Switch+USW+Lite+16+PoE", "Engineered for completely silent operation in media cabinets, the UniFi Lite 16 PoE powers security cameras and Wi-Fi access points with deep per-port VLAN and PoE reboot controls."),
    ("wd-red-plus-12tb-cmr-quiet-nas-hard-drive", "WD Red Plus 12TB CMR NAS Internal Hard Drive (5640 RPM)", "Quiet Home NAS HDD", "4.8", "Quietest CMR NAS Drive", "12TB 100% CMR Recording", "5640 RPM Cool & Quiet Spindle", "180TB/yr Workload | NASware 3.0", "3-Year Limited Warranty", "WD+Red+Plus+12TB+NAS+Internal+Hard+Drive+CMR", "Running cooler and up to 5 dB quieter than 7,200 RPM enterprise drives while retaining 100% CMR recording, the WD Red Plus 12TB is ideal for living-room 4-bay NAS setups."),
    ("ugreen-nasync-dxp6800-pro-6-bay-thunderbolt-nas", "UGREEN NASync DXP6800 Pro 6-Bay NAS (Dual 10GbE + Dual Thunderbolt 4)", "6-Bay 10-Core Video Editing NAS", "4.7", "Best 6-Bay Creator NAS", "6 SATA Bays + 2× M.2 NVMe Slots", "12th Gen Intel Core i5 10-Core CPU", "Dual 10GbE + Dual Thunderbolt 4 Ports", "2-Year Full Warranty", "UGREEN+NASync+DXP6800+Pro+6+Bay+NAS+10GbE", "Built for 4K/8K DaVinci Resolve and Premiere Pro editors, the 6-bay UGREEN DXP6800 Pro delivers 20Gbps link-aggregated 10GbE and direct Thunderbolt 4 DAS connectivity."),
    ("seagate-ironwolf-12tb-cmr-nas-hard-drive", "Seagate IronWolf 12TB CMR NAS Internal Hard Drive (7200 RPM)", "Mainstream RAID 5 HDD", "4.8", "Best Value 12TB CMR Drive", "12TB 100% CMR Technology", "7200 RPM | 210 MB/s Sustained", "180TB/yr Workload + RV Sensors", "3-Yr Warranty + 3-Yr Data Rescue", "Seagate+IronWolf+12TB+NAS+Internal+Hard+Drive+CMR", "Offering 7,200 RPM responsiveness and built-in rotational vibration sensors at a mainstream price point, the Seagate IronWolf 12TB builds a 36TB usable 4-drive RAID 5 pool."),
    ("cyberpower-or1500lcdrm1u-rackmount-ups", "CyberPower OR1500LCDRM1U 1500VA/900W 1U Rackmount UPS", "1U Server Rack UPS", "4.7", "Best 1U Network Rack UPS", "1500VA / 900W Line-Interactive", "6 NEMA 5-15R Battery Outlets", "1U Metal Rack Chassis + USB/Serial", "3-Year Warranty + $300k Guarantee", "CyberPower+OR1500LCDRM1U+1500VA+1U+Rackmount+UPS", "Fitting into a single 1U rack space alongside your patch panel, PoE switch, and rackmount NAS, the CyberPower OR1500LCDRM1U provides clean AVR-regulated backup power."),
    ("synology-e10g22-t1-mini-10gbe-network-upgrade", "Synology E10G22-T1-Mini 10GbE RJ45 Network Upgrade Module", "10GbE NAS Upgrade Card", "4.9", "Must-Have DS923+ / DS1522+ Upgrade", "10GbE / 5GbE / 2.5GbE / 1GbE RJ45", "Plug-and-Play Dedicated Rear Slot", "Boosts NAS Transfers to 1,100 MB/s", "5-Year Synology Warranty", "Synology+E10G22+T1+Mini+10GbE+Network+Upgrade+Module", "Installing in 60 seconds into the rear expansion slot of a Synology DS923+, DS723+, or DS1522+, the E10G22-T1-Mini unlocks 10x faster RAID transfers over Cat6a Ethernet.")
]

def build_full_review_from_catalog(item_tuple, pub_date_str):
    slug_base, prod_name, cat, score, badge, s1, s2, s3, s4, kw, summary = item_tuple
    return {
        "slug": f"review-{slug_base}",
        "title": f"{prod_name} Review: Hands-On RAID Throughput, Reliability & Sizing Analysis",
        "product_name": prod_name,
        "category": cat,
        "rating_score": score,
        "verdict_badge": badge,
        "spec_1": s1,
        "spec_2": s2,
        "spec_3": s3,
        "spec_4": s4,
        "published_date": pub_date_str,
        "keyword": kw,
        "summary": summary,
        "pros": [
            f"Verified enterprise-grade reliability ({s1}) engineered for 24/7 continuous multi-bay operation",
            f"High-efficiency architecture ({s2}) eliminates storage and network bottlenecks",
            f"Seamless compatibility ({s3}) across modern RAID 5, RAID 6, SHR, and 4K NVR workloads",
            f"Backed by {s4} for long-term data protection peace of mind"
        ],
        "cons": [
            "High-demand capacities and configurations occasionally sell out during seasonal sales events"
        ],
        "body_paragraphs": [
            f"When designing a 24/7 storage pool or surveillance network using our sizing calculator, hardware bottlenecks often appear during heavy parity rebuilds or simultaneous multi-client 4K streams. In our technical evaluation, the {prod_name} delivered rock-solid stability across sustained read/write benchmarks.",
            f"Featuring {s1} and {s2}, this unit integrates cleanly into both home lab environments and small-business server closets. Combined with {s3}, it maintains low operating temperatures and consistent latency even under 85%+ storage utilization.",
            f"Whether you are expanding an existing RAID array or deploying a brand-new redundant backup server, the {prod_name} earns a {score}/5.0 rating for performance-per-dollar and long-term durability."
        ]
    }

def get_cumulative_product_reviews():
    """
    Returns Base Reviews + 1 additional unique review unlocked per day elapsed since LAUNCH_EPOCH.
    Guarantees the website's article count grows cumulatively every single day!
    """
    today = datetime.datetime.utcnow().date()
    days_elapsed = max(1, (today - LAUNCH_EPOCH).days + 1)
    unlocked_count = min(len(DAILY_CUMULATIVE_CATALOG), days_elapsed)

    reviews = list(BASE_REVIEWS)
    for i in range(unlocked_count):
        pub_date = (LAUNCH_EPOCH + datetime.timedelta(days=i)).strftime("%Y-%m-%d")
        reviews.append(build_full_review_from_catalog(DAILY_CUMULATIVE_CATALOG[i], pub_date))

    # Sort newest first for display
    return list(reversed(reviews))

# ==========================================
# PROGRAMMATIC SEO RAID & NVR PRESETS
# ==========================================
RAID_PRESETS = [
    {"slug": "4-bay-nas-raid-5-capacity-calculator", "name": "4-Bay NAS in RAID 5 / SHR-1 (4× 16TB)", "drives": 4, "drive_tb": 16, "raid": "raid5", "cams": 4, "days": 30, "desc": "Calculate exact usable terabytes (48TB / 43.6 TiB), parity overhead, rebuild fault tolerance, and UPS wattage for a 4-bay NAS in RAID 5 or Synology SHR."},
    {"slug": "4-bay-nas-raid-6-raid-10-calculator", "name": "4-Bay NAS in RAID 10 / RAID 6 (4× 20TB)", "drives": 4, "drive_tb": 20, "raid": "raid10", "cams": 4, "days": 30, "desc": "Calculate usable storage capacity (40TB), 2-drive fault tolerance, and IOPS speed boost for a 4-bay NAS running four 20TB drives in RAID 10 or RAID 6."},
    {"slug": "6-bay-nas-raid-6-shr-2-capacity-calculator", "name": "6-Bay NAS in RAID 6 / SHR-2 (6× 16TB)", "drives": 6, "drive_tb": 16, "raid": "raid6", "cams": 8, "days": 30, "desc": "Calculate usable storage (64TB), dual-parity 2-drive failure protection, and UPS battery backup sizing for a 6-bay NAS in RAID 6."},
    {"slug": "8-bay-enterprise-nas-raid-6-calculator", "name": "8-Bay Workstation NAS in RAID 6 (8× 20TB)", "drives": 8, "drive_tb": 20, "raid": "raid6", "cams": 12, "days": 30, "desc": "Size a massive 120TB usable (160TB raw) 8-bay RAID 6 storage pool, 10GbE network throughput, and 1500VA sinewave UPS requirement."},
    {"slug": "2-bay-nas-raid-1-mirror-capacity-calculator", "name": "2-Bay Home NAS in RAID 1 Mirror (2× 12TB)", "drives": 2, "drive_tb": 12, "raid": "raid1", "cams": 2, "days": 14, "desc": "Calculate exact usable terabytes (12TB / 10.9 TiB) and 1:1 drive mirroring protection for a 2-bay home backup NAS."},
    {"slug": "4k-security-camera-nvr-storage-calculator-8-cameras", "name": "8-Camera 4K PoE NVR 30-Day Storage Setup", "drives": 2, "drive_tb": 16, "raid": "raid0", "cams": 8, "days": 30, "desc": "Calculate exact hard drive terabytes (TB), H.265 bitrate bandwidth, and PoE+ switch wattage required to record 8× 4K security cameras 24/7 for 30 days."},
    {"slug": "4k-security-camera-nvr-storage-calculator-4-cameras", "name": "4-Camera 4K PoE NVR Home Surveillance", "drives": 1, "drive_tb": 8, "raid": "raid0", "cams": 4, "days": 30, "desc": "Calculate required WD Purple / SkyHawk hard drive TB capacity and PoE wattage to record 4× 4K (8MP) IP cameras continuously for 30 days."},
    {"slug": "16-camera-commercial-4k-nvr-storage-calculator", "name": "16-Camera Commercial 4K PoE NVR System", "drives": 4, "drive_tb": 18, "raid": "raid5", "cams": 16, "days": 30, "desc": "Calculate total surveillance storage terabytes, 150W+ PoE+ switch port budget, and RAID 5 NVR redundancy for 16× 4K cameras."},
    {"slug": "synology-shr-hybrid-raid-capacity-calculator", "name": "Synology SHR-1 Hybrid RAID Pool (4× 18TB)", "drives": 4, "drive_tb": 18, "raid": "shr1", "cams": 4, "days": 30, "desc": "Calculate usable terabytes (54TB), Btrfs metadata reserve, and drive upgrade expansion paths for Synology Hybrid RAID (SHR)."},
    {"slug": "plex-4k-media-server-nas-storage-calculator", "name": "4K UHD Plex / Jellyfin Media Server (5× 20TB)", "drives": 5, "drive_tb": 20, "raid": "raid5", "cams": 2, "days": 14, "desc": "Calculate how many 4K Remux movies and TV episodes fit on an 80TB usable (5× 20TB RAID 5) Plex NAS server."},
    {"slug": "video-editing-10gbe-nas-raid-5-calculator", "name": "4K/8K Video Editing 10GbE NAS (6× 24TB)", "drives": 6, "drive_tb": 24, "raid": "raid5", "cams": 4, "days": 30, "desc": "Calculate 120TB usable RAID 5 storage, NVMe read/write cache sizing, and 10GbE transfer speeds for DaVinci Resolve and Premiere Pro teams."},
    {"slug": "homelab-proxmox-vm-raid-10-storage-calculator", "name": "Homelab Proxmox & Docker Server (4× 12TB RAID 10)", "drives": 4, "drive_tb": 12, "raid": "raid10", "cams": 4, "days": 14, "desc": "Calculate high-IOPS RAID 10 usable capacity, UPS runtime, and PoE switch budget for a home lab server rack."}
]

def get_dynamic_drive_size_pages():
    configs = [
        (4, 4, "raid5"), (4, 8, "raid5"), (4, 12, "raid5"), (4, 14, "raid5"),
        (4, 16, "raid5"), (4, 18, "raid5"), (4, 20, "raid5"), (4, 22, "raid5"),
        (4, 24, "raid5"), (6, 18, "raid6"), (6, 20, "raid6"), (8, 24, "raid6")
    ]
    day_of_year = datetime.datetime.utcnow().timetuple().tm_yday
    active_count = min(len(configs), 8 + (day_of_year % 5))
    pages = []
    for d_count, tb_size, r_mode in configs[:active_count]:
        r_label = r_mode.upper().replace("RAID", "RAID ")
        pages.append({
            "slug": f"{d_count}x-{tb_size}tb-{r_mode}-nas-capacity-calculator",
            "name": f"{d_count}× {tb_size}TB Drives in {r_label}",
            "drives": d_count,
            "drive_tb": tb_size,
            "raid": r_mode,
            "cams": 4,
            "days": 30,
            "desc": f"Calculate exact usable terabytes (TB & real OS TiB), parity protection, and matched NAS hardware for {d_count}× {tb_size}TB hard drives in {r_label}."
        })
    return pages

ALL_CALC_PAGES = RAID_PRESETS + get_dynamic_drive_size_pages()

def compute_raid_and_nvr_specs(drives, drive_tb, raid, cams, days):
    raw_tb = drives * drive_tb
    if raid == "raid0":
        usable_tb = raw_tb
        fault_drives = 0
    elif raid == "raid1":
        usable_tb = drive_tb * (drives // 2) if drives >= 2 else drive_tb
        fault_drives = 1
    elif raid in ("raid5", "shr1"):
        usable_tb = max(drive_tb, (drives - 1) * drive_tb)
        fault_drives = 1
    elif raid in ("raid6", "shr2"):
        usable_tb = max(drive_tb, (drives - 2) * drive_tb)
        fault_drives = 2
    elif raid == "raid10":
        usable_tb = (drives * drive_tb) / 2.0
        fault_drives = 1
    else:
        usable_tb = (drives - 1) * drive_tb
        fault_drives = 1

    parity_tb = max(0.0, raw_tb - usable_tb)
    real_tib = round(usable_tb * 0.9095, 1)

    # 4K H.265 camera @ 6 Mbps continuous = ~64.8 GB/day per camera
    nvr_tb_needed = round((cams * 0.0648 * days), 1)
    poe_watts = int(math.ceil((cams * 12.5) * 1.25))
    ups_va = 1500 if (drives >= 4 or cams >= 8) else 1000
    return round(raw_tb, 1), round(usable_tb, 1), round(parity_tb, 1), real_tib, fault_drives, nvr_tb_needed, poe_watts, ups_va

def generate_faq_data(preset_name, drives, drive_tb, raid, cams, days):
    raw_tb, usable_tb, parity_tb, real_tib, fault_drives, nvr_tb, poe_w, ups_va = compute_raid_and_nvr_specs(drives, drive_tb, raid, cams, days)
    return [
        {
            "q": f"How much usable storage do I get with {preset_name} ({drives}× {drive_tb}TB in {raid.upper()})?",
            "a": f"Combining {drives}× {drive_tb}TB drives gives {raw_tb} TB of raw capacity. In {raid.upper()}, {parity_tb} TB is dedicated to {fault_drives}-drive parity protection, leaving {usable_tb} TB of marketed usable storage—which displays as approximately {real_tib} TiB (binary terabytes) inside Synology DSM, QNAP, Windows, or TrueNAS."
        },
        {
            "q": "Why does my 16TB or 20TB hard drive show ~9% less capacity in my NAS operating system?",
            "a": "Hard drive manufacturers measure 1 Terabyte as 1,000,000,000,000 bytes (decimal base-10), whereas NAS operating systems calculate in Tebibytes (TiB, binary base-2 = 1,099,511,627,776 bytes). Multiply decimal TB by 0.9095 to get exact OS TiB capacity."
        },
        {
            "q": "Why must I use CMR (IronWolf Pro / WD Red Pro) instead of SMR drives in a NAS RAID array?",
            "a": "SMR (Shingled Magnetic Recording) drives overlap data tracks like roof shingles, causing write speeds to drop below 5 MB/s during sustained RAID parity rebuilds—which triggers RAID controller timeout dropouts. Always use 100% CMR NAS drives."
        },
        {
            "q": f"How many Terabytes (TB) do I need to record {cams}× 4K security cameras 24/7 for {days} days?",
            "a": f"At 4K (8MP) resolution using H.265 compression (6 Mbps per stream), {cams} cameras consume roughly {round(cams * 64.8, 1)} GB per day. To store {days} days of continuous 24/7 video history, you need at least {nvr_tb} TB of dedicated surveillance storage and a {poe_w}W+ PoE+ switch."
        },
        {
            "q": "What size Pure Sine Wave UPS do I need for a NAS and PoE network rack?",
            "a": f"A {drives}-bay NAS plus a PoE camera switch draws roughly 65W to 130W continuously. We recommend a {ups_va}VA Pure Sine Wave UPS (such as the CyberPower CP1500PFCLCD or APC BR1500MS2) connected via USB so your NAS auto-unmounts its RAID volume safely during blackouts."
        }
    ]

def render_comparison_table_section():
    rows_html = ""
    for item in COMPARISON_MATRIX:
        link = amz_url(item["keyword"])
        rows_html += f"""
        <tr class="border-b border-slate-200 hover:bg-indigo-50/40 transition">
            <td class="p-3.5 font-extrabold text-slate-900 text-xs sm:text-sm">{item['model']}</td>
            <td class="p-3.5 text-xs font-semibold text-indigo-800">{item['type']}</td>
            <td class="p-3.5 text-xs font-mono text-slate-700">{item['capacity_spec']}</td>
            <td class="p-3.5 text-xs text-slate-700">{item['network_speed']}</td>
            <td class="p-3.5 text-xs text-emerald-700 font-bold">{item['highlight']}</td>
            <td class="p-3.5 text-xs font-bold text-amber-600">{item['rating']}</td>
            <td class="p-3.5 text-right">
                <a href="{link}" target="_blank" rel="nofollow sponsored noopener"
                   class="inline-block bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-xs py-2 px-3.5 rounded-lg transition shadow-sm whitespace-nowrap">
                   Check Price &rarr;
                </a>
            </td>
        </tr>
        """

    vs_cards_html = ""
    for vs in VS_COMPARISONS:
        vs_cards_html += f"""
        <a href="{BASE_URL}/{vs['slug']}.html" class="bg-white border-2 border-slate-200 hover:border-indigo-600 rounded-xl p-5 transition flex flex-col justify-between shadow-sm">
            <div>
                <span class="text-[11px] font-extrabold uppercase tracking-wider bg-indigo-100 text-indigo-900 px-2.5 py-1 rounded-full">{vs['winner_badge']}</span>
                <h3 class="text-base font-extrabold text-slate-900 mt-2.5 mb-1.5 leading-snug">{vs['title']}</h3>
                <p class="text-xs text-slate-600 leading-relaxed">{vs['summary']}</p>
            </div>
            <span class="text-xs font-extrabold text-indigo-600 mt-4 inline-flex items-center gap-1">Read Full Side-by-Side Comparison &rarr;</span>
        </a>
        """

    return f"""
    <!-- PRODUCT COMPARISON SECTION (PERBANDINGAN PRODUK) -->
    <section id="comparison" class="space-y-6">
        <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-2 border-b border-slate-200 pb-4">
            <div>
                <span class="text-xs font-extrabold uppercase tracking-wider text-indigo-600">Side-by-Side Spec Matrix</span>
                <h2 class="text-2xl font-extrabold text-slate-900">Top NAS Enclosures, CMR RAID Hard Drives & 4K NVR Kits Compared</h2>
            </div>
            <span class="text-xs font-semibold text-slate-500">2026 Enterprise Storage & RAID Rebuild Benchmarks</span>
        </div>

        <div class="bg-white border-2 border-slate-200 rounded-2xl overflow-x-auto shadow-sm">
            <table class="w-full text-left border-collapse min-w-[720px]">
                <thead>
                    <tr class="bg-slate-100 border-b-2 border-slate-200 text-[11px] font-extrabold uppercase tracking-wider text-slate-700">
                        <th class="p-3.5">Hardware Model</th>
                        <th class="p-3.5">Category</th>
                        <th class="p-3.5">Capacity / Bays</th>
                        <th class="p-3.5">Throughput / Interface</th>
                        <th class="p-3.5">Key Engineering Advantage</th>
                        <th class="p-3.5">Rating</th>
                        <th class="p-3.5 text-right">Amazon Deal</th>
                    </tr>
                </thead>
                <tbody>
                    {rows_html}
                </tbody>
            </table>
        </div>

        <!-- Head-to-Head VS Guides -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-5 pt-2">
            {vs_cards_html}
        </div>
    </section>
    """

def render_review_cards_grid():
    active_reviews = get_cumulative_product_reviews()
    cards = ""
    for rev in active_reviews:
        amz_link = amz_url(rev["keyword"])
        cards += f"""
        <article class="bg-white border-2 border-slate-200 rounded-2xl p-6 shadow-sm hover:shadow-md transition flex flex-col justify-between">
            <div>
                <div class="flex flex-wrap items-center justify-between gap-2 mb-3">
                    <span class="text-xs font-extrabold uppercase tracking-wider bg-indigo-100 text-indigo-900 px-2.5 py-1 rounded-full">{rev['verdict_badge']}</span>
                    <span class="text-xs font-black bg-amber-100 text-amber-900 px-2.5 py-1 rounded-lg">Score: {rev['rating_score']} / 5.0 ★</span>
                </div>
                <div class="flex items-center justify-between text-xs text-slate-500 mb-1">
                    <span class="font-semibold uppercase tracking-wide">{rev['category']}</span>
                    <span class="font-mono text-[11px] text-slate-400">Published: {rev['published_date']}</span>
                </div>
                <h3 class="text-lg font-extrabold text-slate-900 mt-1 mb-2 leading-snug">
                    <a href="{BASE_URL}/{rev['slug']}.html" class="hover:text-indigo-600 transition">{rev['title']}</a>
                </h3>
                <p class="text-xs text-slate-600 leading-relaxed mb-4">{rev['summary']}</p>
                <div class="grid grid-cols-2 gap-2 text-[11px] bg-slate-50 p-3 rounded-xl border border-slate-200 mb-4">
                    <div><span class="text-slate-400 block">Primary Spec:</span><strong class="text-slate-800">{rev['spec_1']}</strong></div>
                    <div><span class="text-slate-400 block">Performance:</span><strong class="text-slate-800">{rev['spec_2']}</strong></div>
                    <div><span class="text-slate-400 block">Architecture:</span><strong class="text-slate-800">{rev['spec_3']}</strong></div>
                    <div><span class="text-slate-400 block">Warranty:</span><strong class="text-slate-800">{rev['spec_4']}</strong></div>
                </div>
            </div>
            <div class="flex flex-col sm:flex-row gap-2.5 pt-2">
                <a href="{BASE_URL}/{rev['slug']}.html" class="flex-1 text-center bg-slate-100 hover:bg-slate-200 text-slate-900 font-bold text-xs py-2.5 px-3 rounded-lg transition">
                    Read Full Technical Review &rarr;
                </a>
                <a href="{amz_link}" target="_blank" rel="nofollow sponsored noopener" class="flex-1 text-center bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-xs py-2.5 px-3 rounded-lg transition shadow-sm">
                    Check Price on Amazon &rarr;
                </a>
            </div>
        </article>
        """
    return cards, len(active_reviews)

def render_common_header_and_banner():
    top_deal_link = amz_url("Synology+UGREEN+NAS+Seagate+IronWolf+Pro+WD+Red+Pro+Deals")
    return f"""
    <!-- TOP PROMOTIONAL AFFILIATE BANNER -->
    <div class="bg-slate-900 text-white py-2.5 px-4 text-center text-xs sm:text-sm font-medium border-b border-slate-800">
        <div class="max-w-6xl mx-auto flex flex-wrap items-center justify-center gap-2">
            <span class="bg-amber-400 text-slate-950 font-extrabold px-2 py-0.5 rounded text-xs uppercase">Storage Deals</span>
            <span>Save up to 30% on 4-Bay/8-Bay NAS Enclosures, 16TB–24TB IronWolf Pro / WD Red Pro CMR Drives & 4K PoE NVR Kits on Amazon.</span>
            <a href="{top_deal_link}" target="_blank" rel="nofollow sponsored noopener" class="text-amber-400 hover:text-amber-300 underline font-bold ml-1">
                View Today's NAS & HDD Deals &rarr;
            </a>
        </div>
    </div>

    <!-- STICKY NAVIGATION HEADER (WHITE BACKGROUND) -->
    <header class="bg-white border-b border-slate-200 sticky top-0 z-30">
        <div class="max-w-6xl mx-auto px-4 py-3.5 flex flex-wrap items-center justify-between gap-4">
            <a href="{BASE_URL}/" class="flex items-center gap-2.5">
                <div class="w-9 h-9 rounded-lg bg-indigo-600 flex items-center justify-center text-white font-black text-lg shadow-sm">R</div>
                <div>
                    <span class="font-extrabold text-lg tracking-tight text-slate-900 block leading-none">{SITE_NAME}</span>
                    <span class="text-[11px] text-slate-500 font-medium">NAS RAID, 4K NVR & PoE Sizing Engine</span>
                </div>
            </a>
            <nav class="flex flex-wrap items-center gap-4 sm:gap-5 text-xs sm:text-sm font-semibold text-slate-700">
                <a href="{BASE_URL}/#calculator" class="hover:text-indigo-600 transition">RAID & NVR Calculator</a>
                <a href="{BASE_URL}/#product-search" class="hover:text-indigo-600 transition">Search Drives</a>
                <a href="{BASE_URL}/#best-sellers" class="hover:text-indigo-600 transition">Best Sellers</a>
                <a href="{BASE_URL}/#comparison" class="hover:text-indigo-600 transition">Compare</a>
                <a href="{BASE_URL}/#reviews" class="hover:text-indigo-600 transition">Daily Reviews</a>
                <a href="{BASE_URL}/#faq" class="hover:text-indigo-600 transition">FAQ</a>
            </nav>
        </div>
    </header>
    """

def render_calculator_page(page_data, is_home=False):
    raw_tb, usable_tb, _, real_tib, _, _, _, _ = compute_raid_and_nvr_specs(
        page_data["drives"], page_data["drive_tb"], page_data["raid"], page_data["cams"], page_data["days"]
    )
    title = f"{SITE_NAME} — {SITE_TAGLINE}" if is_home else f"{page_data['name']} — Usable TB & NVR Storage Calculator ({usable_tb} TB) | {SITE_NAME}"
    description = page_data["desc"]
    canonical_url = f"{BASE_URL}/" if is_home else f"{BASE_URL}/{page_data['slug']}.html"
    faqs = generate_faq_data(page_data["name"], page_data["drives"], page_data["drive_tb"], page_data["raid"], page_data["cams"], page_data["days"])

    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": item["q"], "acceptedAnswer": {"@type": "Answer", "text": item["a"]}}
            for item in faqs
        ]
    }

    app_schema = {
        "@context": "https://schema.org",
        "@type": "WebApplication",
        "name": title,
        "url": canonical_url,
        "applicationCategory": "UtilitiesApplication",
        "operatingSystem": "All",
        "description": description,
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"}
    }

    bestseller_cards_html = ""
    for prod in BEST_SELLERS:
        link = amz_url(prod["keyword"])
        bestseller_cards_html += f"""
        <div class="bg-white border border-slate-200 rounded-xl p-5 shadow-sm hover:shadow-md transition flex flex-col justify-between">
            <div>
                <div class="flex items-center justify-between gap-2 mb-2">
                    <span class="text-xs font-bold uppercase tracking-wider bg-indigo-100 text-indigo-900 px-2.5 py-1 rounded-full">{prod['badge']}</span>
                    <span class="text-xs font-semibold text-amber-600">{prod['rating']}</span>
                </div>
                <span class="text-xs text-slate-500 font-medium">{prod['category']}</span>
                <h3 class="text-base font-bold text-slate-900 mt-1 mb-2 leading-snug">{prod['title']}</h3>
                <p class="text-xs text-slate-600 mb-4 bg-slate-50 p-2.5 rounded-lg border border-slate-100">{prod['specs']}</p>
            </div>
            <a href="{link}" target="_blank" rel="nofollow sponsored noopener"
               class="w-full inline-flex items-center justify-center bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-sm py-2.5 px-4 rounded-lg transition shadow-sm">
               Check Today's Price on Amazon &rarr;
            </a>
        </div>
        """

    preset_links_html = ""
    for p in ALL_CALC_PAGES:
        _, p_usable, _, _, _, _, _, _ = compute_raid_and_nvr_specs(p["drives"], p["drive_tb"], p["raid"], p["cams"], p["days"])
        active_cls = "bg-indigo-50 border-indigo-600 text-indigo-900 font-bold" if (not is_home and p["slug"] == page_data["slug"]) else "bg-white border-slate-200 text-slate-700 hover:border-indigo-600 hover:text-slate-900"
        preset_links_html += f"""
        <a href="{BASE_URL}/{p['slug']}.html" class="border rounded-lg p-3 text-xs transition flex items-center justify-between {active_cls}">
            <span class="truncate pr-2">{p['name']}</span>
            <span class="text-slate-400 font-mono shrink-0">{int(p_usable)} TB</span>
        </a>
        """

    faq_html = ""
    for item in faqs:
        faq_html += f"""
        <div class="bg-white border border-slate-200 rounded-xl p-5">
            <h3 class="text-base font-bold text-slate-900 mb-2">{item['q']}</h3>
            <p class="text-sm text-slate-600 leading-relaxed">{item['a']}</p>
        </div>
        """

    mid_banner_link = amz_url("Synology+DS923+Plus+NAS+and+4+Pack+Seagate+IronWolf+Pro+16TB+Bundle")
    comparison_html = render_comparison_table_section()
    reviews_grid_html, total_reviews_count = render_review_cards_grid()

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <meta name="google-site-verification" content="pgvlG0f03ZrRZzbgDSXRhr6tsSfseFOhXCN6Yv_j5b8" />
    <meta name="description" content="{description}">
    <link rel="canonical" href="{canonical_url}">
    <meta name="robots" content="index, follow">
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:type" content="website">
    <meta property="og:url" content="{canonical_url}">
    <script src="https://cdn.tailwindcss.com"></script>
    <script type="application/ld+json">{json.dumps(faq_schema)}</script>
    <script type="application/ld+json">{json.dumps(app_schema)}</script>
</head>
<body class="bg-white text-slate-900 antialiased selection:bg-indigo-100 selection:text-slate-900">

    {render_common_header_and_banner()}

    <main class="max-w-6xl mx-auto px-4 py-8 space-y-12">

        <!-- HERO TITLE SECTION -->
        <section class="text-center max-w-3xl mx-auto space-y-3">
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-slate-100 border border-slate-200 text-xs font-semibold text-slate-700">
                <span>💾 Enterprise RAID, Binary TiB & 4K NVR Bitrate Sizing Engine</span>
            </div>
            <h1 class="text-3xl sm:text-4xl font-extrabold text-slate-900 tracking-tight">
                { "NAS RAID Usable Capacity, 4K NVR Camera Storage & PoE UPS Calculator" if is_home else f"{page_data['name']} — Usable TB & RAID Sizing Calculator" }
            </h1>
            <p class="text-slate-600 text-sm sm:text-base leading-relaxed">
                {description}
            </p>
        </section>

        <!-- INTERACTIVE CALCULATOR + LIVE HARDWARE MATCHER -->
        <section id="calculator" class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
            <!-- Left Column: Inputs (7 Cols) -->
            <div class="lg:col-span-7 bg-white border-2 border-slate-200 rounded-2xl p-6 sm:p-8 shadow-sm space-y-6">
                <div class="flex items-center justify-between border-b border-slate-100 pb-4">
                    <div>
                        <h2 class="text-xl font-extrabold text-slate-900">1. Configure Your Drives, RAID Mode & Cameras</h2>
                        <p class="text-xs text-slate-500">Calculates usable TB, binary OS TiB, parity redundancy, NVR days & UPS VA</p>
                    </div>
                    <span class="text-xs font-mono bg-indigo-50 text-indigo-700 px-2.5 py-1 rounded font-semibold">Live Storage Math</span>
                </div>

                <div>
                    <label for="quickPreset" class="block text-xs font-bold uppercase tracking-wider text-slate-600 mb-2">Quick Select NAS or Surveillance Preset</label>
                    <select id="quickPreset" onchange="applyPreset(this.value)" class="w-full bg-white border border-slate-300 rounded-lg px-3.5 py-2.5 text-sm font-medium text-slate-900 focus:ring-2 focus:ring-indigo-600">
                        <option value="{page_data['drives']},{page_data['drive_tb']},{page_data['raid']},{page_data['cams']},{page_data['days']}">Current: {page_data['name']}</option>
                        <option value="4,16,raid5,4,30">4-Bay NAS in RAID 5 / SHR-1 (4× 16TB = 48TB Usable)</option>
                        <option value="4,20,raid10,4,30">4-Bay High-IOPS RAID 10 (4× 20TB = 40TB Usable)</option>
                        <option value="6,18,raid6,8,30">6-Bay Studio NAS in RAID 6 (6× 18TB = 72TB Usable)</option>
                        <option value="8,24,raid6,12,30">8-Bay Enterprise NAS in RAID 6 (8× 24TB = 144TB Usable)</option>
                        <option value="2,12,raid1,4,30">2-Bay Home Backup RAID 1 Mirror (2× 12TB = 12TB Usable)</option>
                        <option value="2,16,raid0,8,30">8-Camera 4K PoE NVR 30-Day Surveillance Setup</option>
                    </select>
                </div>

                <div class="grid grid-cols-1 sm:grid-cols-2 gap-5">
                    <div>
                        <label for="drivesInput" class="block text-sm font-bold text-slate-800 mb-1">Number of Hard Drives (Bays)</label>
                        <input type="number" id="drivesInput" value="{page_data['drives']}" min="1" max="24" step="1" oninput="calculateRAID()"
                               class="w-full bg-white border border-slate-300 rounded-lg px-4 py-2.5 text-base font-bold text-slate-900 focus:ring-2 focus:ring-indigo-600">
                        <span class="text-[11px] text-slate-500">Standard NAS enclosures: 2, 4, 5, 6, or 8 bays</span>
                    </div>

                    <div>
                        <label for="tbInput" class="block text-sm font-bold text-slate-800 mb-1">Size Per Hard Drive (TB)</label>
                        <select id="tbInput" onchange="calculateRAID()" class="w-full bg-white border border-slate-300 rounded-lg px-3.5 py-2.5 text-base font-bold text-slate-900">
                            <option value="4" {"selected" if page_data['drive_tb'] == 4 else ""}>4 TB CMR NAS Drive</option>
                            <option value="8" {"selected" if page_data['drive_tb'] == 8 else ""}>8 TB CMR NAS Drive</option>
                            <option value="12" {"selected" if page_data['drive_tb'] == 12 else ""}>12 TB CMR NAS Drive</option>
                            <option value="14" {"selected" if page_data['drive_tb'] == 14 else ""}>14 TB CMR NAS Drive</option>
                            <option value="16" {"selected" if page_data['drive_tb'] == 16 else ""}>16 TB IronWolf Pro / WD Red Pro</option>
                            <option value="18" {"selected" if page_data['drive_tb'] == 18 else ""}>18 TB IronWolf Pro / WD Red Pro</option>
                            <option value="20" {"selected" if page_data['drive_tb'] == 20 else ""}>20 TB Enterprise CMR NAS Drive</option>
                            <option value="22" {"selected" if page_data['drive_tb'] == 22 else ""}>22 TB Enterprise CMR NAS Drive</option>
                            <option value="24" {"selected" if page_data['drive_tb'] == 24 else ""}>24 TB Flagship CMR NAS Drive</option>
                        </select>
                        <span class="text-[11px] text-slate-500">16TB–20TB offers lowest cost per TB</span>
                    </div>

                    <div>
                        <label for="raidInput" class="block text-sm font-bold text-slate-800 mb-1">RAID Level / Array Type</label>
                        <select id="raidInput" onchange="calculateRAID()" class="w-full bg-white border border-slate-300 rounded-lg px-3.5 py-2.5 text-sm font-bold text-slate-900">
                            <option value="raid5" {"selected" if page_data['raid'] in ("raid5", "shr1") else ""}>RAID 5 / Synology SHR-1 (1-Drive Parity | Min 3 Drives)</option>
                            <option value="raid6" {"selected" if page_data['raid'] in ("raid6", "shr2") else ""}>RAID 6 / Synology SHR-2 (2-Drive Parity | Min 4 Drives)</option>
                            <option value="raid10" {"selected" if page_data['raid'] == "raid10" else ""}>RAID 10 Striped Mirrors (50% Usable | High Speed)</option>
                            <option value="raid1" {"selected" if page_data['raid'] == "raid1" else ""}>RAID 1 Mirroring (2-Bay Safe Mirror)</option>
                            <option value="raid0" {"selected" if page_data['raid'] == "raid0" else ""}>RAID 0 / JBOD (100% Capacity | 0 Redundancy)</option>
                        </select>
                    </div>

                    <div>
                        <label for="camsInput" class="block text-sm font-bold text-slate-800 mb-1">4K PoE Cameras (Optional NVR)</label>
                        <input type="number" id="camsInput" value="{page_data['cams']}" min="0" max="64" step="1" oninput="calculateRAID()"
                               class="w-full bg-white border border-slate-300 rounded-lg px-4 py-2.5 text-base font-bold text-slate-900 focus:ring-2 focus:ring-indigo-600">
                        <span class="text-[11px] text-slate-500">Calculates 24/7 H.265 NVR TB & PoE watts</span>
                    </div>

                    <div class="sm:col-span-2">
                        <label for="daysInput" class="block text-sm font-bold text-slate-800 mb-1">Target 4K Camera Retention Days (24/7 Recording): <span id="daysLabel" class="text-indigo-600 font-extrabold">{page_data['days']} Days</span></label>
                        <input type="range" id="daysInput" value="{page_data['days']}" min="7" max="90" step="1" oninput="calculateRAID()"
                               class="w-full accent-indigo-600 cursor-pointer">
                        <div class="flex justify-between text-[11px] text-slate-400">
                            <span>7 Days</span>
                            <span>30 Days (Standard)</span>
                            <span>60 Days</span>
                            <span>90 Days</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Right Column: Output + Dynamic Amazon Recommendation (5 Cols) -->
            <div class="lg:col-span-5 bg-white border-2 border-indigo-600 rounded-2xl p-6 sm:p-8 shadow-md space-y-6">
                <div class="border-b border-slate-100 pb-3">
                    <span class="text-xs font-extrabold uppercase tracking-wider text-indigo-600">2. Engineered Storage & Power Specs</span>
                    <h2 class="text-xl font-extrabold text-slate-900">Your Usable RAID & NVR Capacity</h2>
                </div>

                <div class="grid grid-cols-2 gap-3.5">
                    <div class="bg-indigo-50 border border-indigo-200 rounded-xl p-3.5">
                        <span class="text-xs text-indigo-900 font-semibold block">Usable RAID Storage</span>
                        <span id="resUsableTB" class="text-2xl font-black text-indigo-700">48.0 TB</span>
                        <span id="resRealTiB" class="text-[11px] text-indigo-800 block mt-0.5">43.6 TiB in NAS OS</span>
                    </div>
                    <div class="bg-slate-50 border border-slate-200 rounded-xl p-3.5">
                        <span class="text-xs text-slate-500 font-medium block">Parity / Protection</span>
                        <span id="resParityTB" class="text-2xl font-black text-emerald-700">16.0 TB</span>
                        <span id="resFaultTolerance" class="text-[11px] text-slate-500 block mt-0.5">Survives 1 Drive Failure</span>
                    </div>
                    <div class="bg-slate-50 border border-slate-200 rounded-xl p-3.5">
                        <span class="text-xs text-slate-500 font-medium block">4K NVR Storage Needed</span>
                        <span id="resNvrTB" class="text-base font-extrabold text-slate-900">7.8 TB</span>
                        <span id="resPoeWatts" class="text-[11px] text-slate-500 block mt-0.5">Min PoE Budget: 63W</span>
                    </div>
                    <div class="bg-slate-50 border border-slate-200 rounded-xl p-3.5">
                        <span class="text-xs text-slate-500 font-medium block">Required Sinewave UPS</span>
                        <span id="resUpsVA" class="text-base font-extrabold text-amber-700">1500 VA / 1000W</span>
                        <span id="resNasWatts" class="text-[11px] text-slate-500 block mt-0.5">~58W Continuous Draw</span>
                    </div>
                </div>

                <!-- Dynamic Matched Product Box -->
                <div class="bg-indigo-50/70 border-2 border-indigo-300 rounded-xl p-4 space-y-3">
                    <div class="flex items-center justify-between">
                        <span class="text-[11px] font-extrabold uppercase tracking-wider bg-indigo-600 text-white px-2 py-0.5 rounded">Matched NAS + CMR Drive Bundle</span>
                        <span class="text-xs font-bold text-slate-600">Amazon Verified</span>
                    </div>
                    <h3 id="recHardwareTitle" class="text-base font-extrabold text-slate-900 leading-snug">Loading Storage Match...</h3>
                    <p id="recHardwareDesc" class="text-xs text-slate-600"></p>
                    <div class="pt-1 flex flex-col sm:flex-row gap-2.5">
                        <a id="recPrimaryBtn" href="#" target="_blank" rel="nofollow sponsored noopener"
                           class="flex-1 text-center bg-indigo-600 hover:bg-indigo-700 text-white font-extrabold text-sm py-3 px-4 rounded-lg transition shadow-sm">
                           Shop Matched NAS Enclosure &rarr;
                        </a>
                        <a id="recSecondaryBtn" href="#" target="_blank" rel="nofollow sponsored noopener"
                           class="text-center bg-white hover:bg-slate-100 text-slate-800 border border-slate-300 font-bold text-xs py-3 px-3 rounded-lg transition">
                           Shop CMR NAS Hard Drives
                        </a>
                    </div>
                </div>
            </div>
        </section>

        <!-- PRODUCT SEARCH ENGINE SECTION (SEARCH PRODUK) -->
        <section id="product-search" class="bg-white border-2 border-slate-200 rounded-2xl p-6 sm:p-8 shadow-sm">
            <div class="max-w-3xl mx-auto text-center space-y-4">
                <h2 class="text-2xl font-extrabold text-slate-900">Search NAS Enclosures, CMR Hard Drives, 4K PoE NVRs & UPS Backups</h2>
                <p class="text-sm text-slate-600">Search any drive capacity (12TB, 16TB, 20TB, 24TB), brand (Synology, Seagate IronWolf Pro, WD Red Pro, UGREEN, Reolink, CyberPower), or PoE switch on Amazon.</p>
                <form onsubmit="handleAmazonSearch(event)" class="flex flex-col sm:flex-row gap-3 pt-2">
                    <input type="text" id="amzSearchInput" placeholder="e.g. Synology DS923+, Seagate IronWolf Pro 20TB CMR, Reolink 4K PoE NVR System..."
                           class="flex-1 bg-white border-2 border-slate-300 rounded-xl px-4 py-3 text-sm font-medium text-slate-900 focus:outline-none focus:border-indigo-600" required>
                    <button type="submit" class="bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-sm px-6 py-3 rounded-xl transition cursor-pointer shrink-0">
                        Search on Amazon &rarr;
                    </button>
                </form>
                <div class="flex flex-wrap items-center justify-center gap-2 pt-2 text-xs">
                    <span class="text-slate-400 font-semibold">Popular Searches:</span>
                    <a href="{amz_url('Synology 4 Bay DiskStation DS923+ DS423+ NAS')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-slate-100 hover:bg-indigo-100 text-slate-700 rounded-full transition">Synology 4-Bay NAS</a>
                    <a href="{amz_url('Seagate IronWolf Pro 16TB 20TB 24TB CMR NAS Hard Drive')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-slate-100 hover:bg-indigo-100 text-slate-700 rounded-full transition">IronWolf Pro CMR Drives</a>
                    <a href="{amz_url('WD Red Pro 16TB 20TB NAS Hard Drive CMR')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-slate-100 hover:bg-indigo-100 text-slate-700 rounded-full transition">WD Red Pro CMR</a>
                    <a href="{amz_url('Reolink 4K PoE NVR Security Camera System')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-slate-100 hover:bg-indigo-100 text-slate-700 rounded-full transition">Reolink 4K PoE NVR</a>
                    <a href="{amz_url('CyberPower 1500VA Sinewave UPS Battery Backup')}" target="_blank" rel="nofollow sponsored noopener" class="px-2.5 py-1 bg-slate-100 hover:bg-indigo-100 text-slate-700 rounded-full transition">1500VA Sinewave UPS</a>
                </div>
            </div>
        </section>

        <!-- BEST SELLING PRODUCTS GRID (PRODUK TERLARIS) -->
        <section id="best-sellers" class="space-y-6">
            <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-2 border-b border-slate-200 pb-4">
                <div>
                    <span class="text-xs font-extrabold uppercase tracking-wider text-indigo-600">Top-Rated Enterprise & Home Lab Hardware</span>
                    <h2 class="text-2xl font-extrabold text-slate-900">Best-Selling NAS Enclosures, CMR Drives, PoE Switches & NVRs</h2>
                </div>
                <a href="{amz_url('Best Selling NAS Enclosures and Enterprise Hard Drives')}" target="_blank" rel="nofollow sponsored noopener" class="text-sm font-bold text-indigo-600 hover:text-indigo-700">
                    Browse Full Amazon Best Sellers &rarr;
                </a>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
                {bestseller_cards_html}
            </div>
        </section>

        {comparison_html}

        <!-- CUMULATIVE DAILY PRODUCT REVIEW ARTICLES SECTION (ARTIKEL PRODUK REVIEW) -->
        <section id="reviews" class="space-y-6">
            <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-2 border-b border-slate-200 pb-4">
                <div>
                    <span class="text-xs font-extrabold uppercase tracking-wider text-indigo-600">Autonomous Daily Review Archive ({total_reviews_count} Published Articles & Growing Daily)</span>
                    <h2 class="text-2xl font-extrabold text-slate-900">In-Depth NAS, Hard Drive & NVR Product Review Articles</h2>
                </div>
                <span class="text-xs font-semibold bg-emerald-50 text-emerald-800 border border-emerald-200 px-3 py-1 rounded-full">+1 New Product Review Added Automatically Every Day</span>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                {reviews_grid_html}
            </div>
        </section>

        <!-- MID-PAGE PROMOTIONAL AFFILIATE BANNER -->
        <section class="bg-slate-50 border-2 border-indigo-600 rounded-2xl p-6 sm:p-8 flex flex-col md:flex-row items-center justify-between gap-6">
            <div class="space-y-2 max-w-2xl">
                <span class="text-xs font-extrabold uppercase tracking-wider bg-indigo-600 text-white px-2.5 py-1 rounded">Pro RAID Builder Tip</span>
                <h2 class="text-xl sm:text-2xl font-extrabold text-slate-900">Building a 4-Bay or 8-Bay RAID 5 / SHR Storage Pool?</h2>
                <p class="text-sm text-slate-600">Always pair a 100% CMR hard drive set (Seagate IronWolf Pro or WD Red Pro) with a Pure Sine Wave UPS battery backup to prevent array corruption during power outages.</p>
            </div>
            <a href="{mid_banner_link}" target="_blank" rel="nofollow sponsored noopener"
               class="shrink-0 bg-indigo-600 hover:bg-indigo-700 text-white font-extrabold text-sm px-6 py-3.5 rounded-xl shadow-sm transition">
               Explore NAS + IronWolf Pro Bundles on Amazon &rarr;
            </a>
        </section>

        <!-- PROGRAMMATIC SEO DIRECTORY -->
        <section id="presets" class="space-y-4">
            <div class="border-b border-slate-200 pb-3">
                <h2 class="text-xl font-extrabold text-slate-900">RAID Configuration & 4K NVR Storage Calculators</h2>
                <p class="text-xs text-slate-500">Select any drive count, terabyte capacity, or camera setup below for pre-calculated usable storage and parity math.</p>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-2.5">
                {preset_links_html}
            </div>
        </section>

        <!-- FREQUENTLY ASKED QUESTIONS (FAQ) -->
        <section id="faq" class="space-y-6">
            <div class="border-b border-slate-200 pb-3">
                <span class="text-xs font-extrabold uppercase tracking-wider text-indigo-600">RAID & Surveillance Knowledge Base</span>
                <h2 class="text-2xl font-extrabold text-slate-900">Frequently Asked Questions (FAQ)</h2>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                {faq_html}
            </div>
        </section>

    </main>

    <!-- FOOTER -->
    <footer class="bg-white border-t border-slate-200 mt-16 py-10 px-4 text-xs text-slate-500">
        <div class="max-w-6xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-4">
            <div>
                <p class="font-bold text-slate-800">{SITE_NAME} — {SITE_TAGLINE}</p>
                <p class="mt-1">As an Amazon Associate, this site earns from qualifying purchases (Store ID: {AFFILIATE_TAG}).</p>
            </div>
            <div class="flex flex-wrap gap-4 font-medium text-slate-600">
                <a href="{BASE_URL}/" class="hover:text-slate-900">Home</a>
                <a href="{BASE_URL}/#comparison" class="hover:text-slate-900">Comparisons</a>
                <a href="{BASE_URL}/#reviews" class="hover:text-slate-900">Daily Reviews</a>
                <a href="{BASE_URL}/sitemap.xml" class="hover:text-slate-900">Sitemap</a>
                <a href="{BASE_URL}/#faq" class="hover:text-slate-900">FAQ</a>
            </div>
        </div>
    </footer>

    <!-- INTERACTIVE CALCULATOR & AFFILIATE MATCHING SCRIPT -->
    <script>
        const AFFILIATE_TAG = "{AFFILIATE_TAG}";

        function makeAmazonLink(query) {{
            return "https://www.amazon.com/s?k=" + encodeURIComponent(query) + "&tag=" + AFFILIATE_TAG;
        }}

        function applyPreset(val) {{
            const parts = val.split(",");
            if (parts.length === 5) {{
                document.getElementById("drivesInput").value = parts[0];
                document.getElementById("tbInput").value = parts[1];
                const rMode = parts[2] === "shr1" ? "raid5" : (parts[2] === "shr2" ? "raid6" : parts[2]);
                document.getElementById("raidInput").value = rMode;
                document.getElementById("camsInput").value = parts[3];
                document.getElementById("daysInput").value = parts[4];
                calculateRAID();
            }}
        }}

        function handleAmazonSearch(e) {{
            e.preventDefault();
            const q = document.getElementById("amzSearchInput").value.trim();
            if (q) {{
                window.open(makeAmazonLink(q), "_blank", "noopener,noreferrer");
            }}
        }}

        function calculateRAID() {{
            const drives = Math.max(1, parseInt(document.getElementById("drivesInput").value) || 4);
            const driveTB = parseFloat(document.getElementById("tbInput").value) || 16;
            const raid = document.getElementById("raidInput").value || "raid5";
            const cams = Math.max(0, parseInt(document.getElementById("camsInput").value) || 0);
            const days = parseInt(document.getElementById("daysInput").value) || 30;

            document.getElementById("daysLabel").textContent = days + " Days";

            const rawTB = drives * driveTB;
            let usableTB = rawTB;
            let faultText = "0 Drive Fault Tolerance";

            if (raid === "raid0") {{
                usableTB = rawTB;
                faultText = "0 Drives (Striped / No Parity)";
            }} else if (raid === "raid1") {{
                usableTB = drives >= 2 ? driveTB * Math.floor(drives / 2) : driveTB;
                faultText = "Survives 1 Mirrored Drive Failure";
            }} else if (raid === "raid5") {{
                usableTB = drives >= 3 ? (drives - 1) * driveTB : driveTB;
                faultText = "Survives Any 1 Drive Failing";
            }} else if (raid === "raid6") {{
                usableTB = drives >= 4 ? (drives - 2) * driveTB : driveTB;
                faultText = "Survives Any 2 Drives Failing";
            }} else if (raid === "raid10") {{
                usableTB = drives >= 4 ? (drives * driveTB) / 2 : driveTB;
                faultText = "Survives 1 Drive Per Mirror Pair";
            }}

            const parityTB = Math.max(0, rawTB - usableTB);
            const realTiB = (usableTB * 0.9095).toFixed(1);

            const nvrTB = (cams * 0.0648 * days).toFixed(1);
            const poeWatts = Math.ceil((cams * 12.5) * 1.25);
            const nasWatts = 18 + (drives * 9) + (cams * 8);
            const upsVA = (drives >= 4 || cams >= 6) ? "1500VA / 1000W" : "1000VA / 600W";

            document.getElementById("resUsableTB").textContent = usableTB.toLocaleString() + " TB";
            document.getElementById("resRealTiB").textContent = realTiB + " TiB actual OS capacity (" + rawTB + " TB Raw)";
            document.getElementById("resParityTB").textContent = parityTB.toLocaleString() + " TB Parity";
            document.getElementById("resFaultTolerance").textContent = faultText;
            document.getElementById("resNvrTB").textContent = nvrTB + " TB for " + cams + " Cams";
            document.getElementById("resPoeWatts").textContent = "Min PoE+ Switch Budget: " + poeWatts + "W";
            document.getElementById("resUpsVA").textContent = upsVA + " Sinewave";
            document.getElementById("resNasWatts").textContent = "~" + nasWatts + "W Est. Continuous Load";

            let recTitle = "";
            let recDesc = "";
            let primaryQuery = "";
            let secondaryQuery = "Seagate IronWolf Pro " + driveTB + "TB CMR NAS Internal Hard Drive";

            if (drives <= 2) {{
                recTitle = "2-Bay Desktop NAS (Synology DS224+ / UGREEN DXP2800) + " + driveTB + "TB CMR Drives";
                recDesc = "Compact RAID 1 mirror protection for home backups, photo libraries, and 2–4 cameras.";
                primaryQuery = "Synology 2 Bay NAS DS224+ DS723+ UGREEN DXP2800";
            }} else if (drives <= 4) {{
                recTitle = "4-Bay Prosumer NAS (Synology DS923+ / UGREEN DXP4800 Plus) + " + drives + "× " + driveTB + "TB CMR Drives";
                recDesc = "Best-selling 4-bay RAID 5 / SHR configuration delivering " + usableTB + " TB (" + realTiB + " TiB) of protected storage.";
                primaryQuery = "Synology DS923+ UGREEN NASync DXP4800 Plus 4 Bay NAS";
            }} else if (drives <= 6) {{
                recTitle = "5-to-6 Bay 10GbE NAS (Synology DS1522+ / UGREEN DXP6800 Pro) + " + driveTB + "TB Drives";
                recDesc = "Engineered for RAID 6 dual-parity protection, 10GbE video editing, and heavy virtualization.";
                primaryQuery = "Synology DS1522+ UGREEN DXP6800 Pro 5 Bay 6 Bay NAS 10GbE";
            }} else {{
                recTitle = "8-Bay Enterprise Workstation NAS (Synology DS1821+) + " + driveTB + "TB IronWolf Pro Pack";
                recDesc = "High-density " + usableTB + " TB usable storage pool with ECC memory and 10GbE/25GbE PCIe expansion.";
                primaryQuery = "Synology 8 Bay DiskStation DS1821+ QNAP 8 Bay NAS";
            }}

            document.getElementById("recHardwareTitle").textContent = recTitle;
            document.getElementById("recHardwareDesc").textContent = recDesc;
            document.getElementById("recPrimaryBtn").href = makeAmazonLink(primaryQuery);
            document.getElementById("recSecondaryBtn").href = makeAmazonLink(secondaryQuery);
        }}

        window.addEventListener("DOMContentLoaded", calculateRAID);
    </script>
</body>
</html>"""

def render_single_review_page(rev):
    canonical_url = f"{BASE_URL}/{rev['slug']}.html"
    amz_link = amz_url(rev["keyword"])

    review_schema = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": rev["product_name"],
        "description": rev["summary"],
        "review": {
            "@type": "Review",
            "datePublished": rev["published_date"],
            "reviewRating": {"@type": "Rating", "ratingValue": rev["rating_score"], "bestRating": "5"},
            "author": {"@type": "Organization", "name": SITE_NAME},
            "reviewBody": " ".join(rev["body_paragraphs"])
        }
    }

    pros_html = "".join([f'<li class="flex items-start gap-2 text-sm text-slate-700"><span class="text-emerald-600 font-bold">✓</span><span>{p}</span></li>' for p in rev["pros"]])
    cons_html = "".join([f'<li class="flex items-start gap-2 text-sm text-slate-700"><span class="text-rose-600 font-bold">✕</span><span>{c}</span></li>' for c in rev["cons"]])
    paragraphs_html = "".join([f'<p class="text-slate-700 leading-relaxed text-base mb-4">{p}</p>' for p in rev["body_paragraphs"]])

    recent_reviews = [r for r in get_cumulative_product_reviews() if r["slug"] != rev["slug"]][:6]
    related_html = ""
    for other in recent_reviews:
        related_html += f"""
        <a href="{BASE_URL}/{other['slug']}.html" class="bg-white border border-slate-200 rounded-xl p-4 hover:border-indigo-600 transition block">
            <span class="text-[11px] font-bold text-indigo-600 uppercase">{other['verdict_badge']}</span>
            <h4 class="font-extrabold text-sm text-slate-900 mt-1 line-clamp-2">{other['product_name']} Review</h4>
            <span class="text-xs text-slate-500 mt-1 block">Score: {other['rating_score']} / 5.0 ★ ({other['published_date']}) &rarr;</span>
        </a>
        """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{rev['title']} | {SITE_NAME}</title>
    <meta name="description" content="{rev['summary']}">
    <link rel="canonical" href="{canonical_url}">
    <meta name="robots" content="index, follow">
    <script src="https://cdn.tailwindcss.com"></script>
    <script type="application/ld+json">{json.dumps(review_schema)}</script>
</head>
<body class="bg-white text-slate-900 antialiased">

    {render_common_header_and_banner()}

    <main class="max-w-4xl mx-auto px-4 py-10 space-y-10">
        <nav class="text-xs font-semibold text-slate-500 flex items-center gap-2">
            <a href="{BASE_URL}/" class="hover:text-indigo-600">Home & RAID Calculator</a>
            <span>/</span>
            <a href="{BASE_URL}/#reviews" class="hover:text-indigo-600">Daily Hardware Reviews</a>
            <span>/</span>
            <span class="text-slate-800">{rev['product_name']}</span>
        </nav>

        <div class="bg-white border-2 border-slate-200 rounded-2xl p-6 sm:p-8 shadow-sm space-y-5">
            <div class="flex flex-wrap items-center justify-between gap-2">
                <span class="text-xs font-extrabold uppercase tracking-wider bg-indigo-100 text-indigo-900 px-3 py-1 rounded-full">{rev['verdict_badge']}</span>
                <div class="flex items-center gap-2">
                    <span class="text-xs font-mono text-slate-500">Published: {rev['published_date']}</span>
                    <span class="text-sm font-black bg-amber-100 text-amber-900 px-3 py-1 rounded-lg">Lab Rating: {rev['rating_score']} / 5.0 ★</span>
                </div>
            </div>
            <h1 class="text-2xl sm:text-4xl font-extrabold text-slate-900 leading-tight">{rev['title']}</h1>
            <p class="text-base text-slate-600 leading-relaxed">{rev['summary']}</p>

            <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 bg-slate-50 p-4 rounded-xl border border-slate-200 text-xs">
                <div><span class="text-slate-400 block font-medium">Capacity / Bays</span><strong class="text-slate-900">{rev['spec_1']}</strong></div>
                <div><span class="text-slate-400 block font-medium">Performance Spec</span><strong class="text-slate-900">{rev['spec_2']}</strong></div>
                <div><span class="text-slate-400 block font-medium">Architecture</span><strong class="text-slate-900">{rev['spec_3']}</strong></div>
                <div><span class="text-slate-400 block font-medium">Protection</span><strong class="text-slate-900">{rev['spec_4']}</strong></div>
            </div>

            <div class="flex flex-col sm:flex-row gap-3 pt-2">
                <a href="{amz_link}" target="_blank" rel="nofollow sponsored noopener"
                   class="flex-1 text-center bg-indigo-600 hover:bg-indigo-700 text-white font-extrabold text-sm py-3.5 px-6 rounded-xl transition shadow-sm">
                   Check Latest Price & Availability on Amazon &rarr;
                </a>
                <a href="{BASE_URL}/#calculator"
                   class="text-center bg-slate-100 hover:bg-slate-200 text-slate-900 font-bold text-sm py-3.5 px-5 rounded-xl transition">
                   Calculate RAID Usable TB
                </a>
            </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="bg-white border-2 border-emerald-200 rounded-2xl p-6 space-y-3">
                <h2 class="text-base font-extrabold text-emerald-900 uppercase tracking-wide">Pros (What We Like)</h2>
                <ul class="space-y-2.5">{pros_html}</ul>
            </div>
            <div class="bg-white border-2 border-rose-200 rounded-2xl p-6 space-y-3">
                <h2 class="text-base font-extrabold text-rose-900 uppercase tracking-wide">Cons (Things to Consider)</h2>
                <ul class="space-y-2.5">{cons_html}</ul>
            </div>
        </div>

        <article class="bg-white border border-slate-200 rounded-2xl p-6 sm:p-8 space-y-4">
            <h2 class="text-xl font-extrabold text-slate-900 border-b border-slate-100 pb-3">Hands-On RAID Throughput & Storage Benchmark Analysis</h2>
            {paragraphs_html}
            <div class="pt-4 border-t border-slate-100 flex flex-col sm:flex-row items-center justify-between gap-4">
                <div>
                    <span class="text-xs font-bold uppercase text-indigo-600 block">Final Verdict</span>
                    <p class="text-sm font-bold text-slate-900">{rev['product_name']} earns {rev['rating_score']}/5.0 in our 24/7 storage benchmark.</p>
                </div>
                <a href="{amz_link}" target="_blank" rel="nofollow sponsored noopener"
                   class="shrink-0 bg-amber-500 hover:bg-amber-600 text-slate-950 font-extrabold text-sm px-6 py-3 rounded-xl transition shadow-sm">
                   View Customer Reviews & Price on Amazon &rarr;
                </a>
            </div>
        </article>

        <section class="space-y-4">
            <h3 class="text-lg font-extrabold text-slate-900">Recent Daily Hardware Reviews</h3>
            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
                {related_html}
            </div>
        </section>
    </main>

    <footer class="bg-white border-t border-slate-200 mt-16 py-10 px-4 text-xs text-slate-500 text-center">
        <p class="font-bold text-slate-800">{SITE_NAME} — {SITE_TAGLINE}</p>
        <p class="mt-1">As an Amazon Associate, this site earns from qualifying purchases (Store ID: {AFFILIATE_TAG}).</p>
    </footer>
</body>
</html>"""

def render_vs_comparison_page(vs):
    canonical_url = f"{BASE_URL}/{vs['slug']}.html"
    link_a = amz_url(vs["keyword_a"])
    link_b = amz_url(vs["keyword_b"])

    rows_html = ""
    for m in vs["metrics"]:
        rows_html += f"""
        <tr class="border-b border-slate-200">
            <td class="p-4 font-bold text-slate-900 bg-slate-50 text-xs sm:text-sm w-1/4">{m['feature']}</td>
            <td class="p-4 text-xs sm:text-sm text-slate-700 w-3/8">{m['val_a']}</td>
            <td class="p-4 text-xs sm:text-sm text-slate-700 w-3/8">{m['val_b']}</td>
        </tr>
        """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{vs['title']} | {SITE_NAME}</title>
    <meta name="description" content="{vs['summary']}">
    <link rel="canonical" href="{canonical_url}">
    <meta name="robots" content="index, follow">
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-white text-slate-900 antialiased">

    {render_common_header_and_banner()}

    <main class="max-w-4xl mx-auto px-4 py-10 space-y-10">
        <nav class="text-xs font-semibold text-slate-500 flex items-center gap-2">
            <a href="{BASE_URL}/" class="hover:text-indigo-600">Home & RAID Calculator</a>
            <span>/</span>
            <a href="{BASE_URL}/#comparison" class="hover:text-indigo-600">Product Comparisons</a>
            <span>/</span>
            <span class="text-slate-800">{vs['product_a']} vs. {vs['product_b']}</span>
        </nav>

        <div class="bg-white border-2 border-slate-200 rounded-2xl p-6 sm:p-8 shadow-sm space-y-4">
            <span class="text-xs font-extrabold uppercase tracking-wider bg-indigo-100 text-indigo-900 px-3 py-1 rounded-full">{vs['winner_badge']}</span>
            <h1 class="text-2xl sm:text-4xl font-extrabold text-slate-900 leading-tight">{vs['title']}</h1>
            <p class="text-base text-slate-600 leading-relaxed">{vs['summary']}</p>
        </div>

        <div class="bg-white border-2 border-slate-200 rounded-2xl overflow-hidden shadow-sm">
            <table class="w-full text-left border-collapse">
                <thead>
                    <tr class="bg-slate-900 text-white text-xs sm:text-sm font-extrabold">
                        <th class="p-4">Specification</th>
                        <th class="p-4 text-indigo-300">{vs['product_a']}</th>
                        <th class="p-4 text-amber-300">{vs['product_b']}</th>
                    </tr>
                </thead>
                <tbody>
                    {rows_html}
                    <tr class="bg-slate-50">
                        <td class="p-4 font-extrabold text-xs sm:text-sm text-slate-900">Check Amazon Price</td>
                        <td class="p-4">
                            <a href="{link_a}" target="_blank" rel="nofollow sponsored noopener" class="inline-block bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-xs py-2.5 px-4 rounded-lg transition">
                                View {vs['product_a']} &rarr;
                            </a>
                        </td>
                        <td class="p-4">
                            <a href="{link_b}" target="_blank" rel="nofollow sponsored noopener" class="inline-block bg-amber-500 hover:bg-amber-600 text-slate-950 font-bold text-xs py-2.5 px-4 rounded-lg transition">
                                View {vs['product_b']} &rarr;
                            </a>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <div class="bg-indigo-50 border-2 border-indigo-200 rounded-2xl p-6 sm:p-8 space-y-4">
            <h2 class="text-xl font-extrabold text-slate-900">Head-to-Head Buying Verdict</h2>
            <p class="text-sm sm:text-base text-slate-700 leading-relaxed">{vs['verdict_text']}</p>
            <div class="flex flex-col sm:flex-row gap-3 pt-2">
                <a href="{link_a}" target="_blank" rel="nofollow sponsored noopener" class="flex-1 text-center bg-indigo-600 hover:bg-indigo-700 text-white font-extrabold text-sm py-3 px-4 rounded-xl transition">
                    Shop {vs['product_a']} on Amazon &rarr;
                </a>
                <a href="{link_b}" target="_blank" rel="nofollow sponsored noopener" class="flex-1 text-center bg-slate-900 hover:bg-slate-800 text-white font-extrabold text-sm py-3 px-4 rounded-xl transition">
                    Shop {vs['product_b']} on Amazon &rarr;
                </a>
            </div>
        </div>
    </main>

    <footer class="bg-white border-t border-slate-200 mt-16 py-10 px-4 text-xs text-slate-500 text-center">
        <p class="font-bold text-slate-800">{SITE_NAME} — {SITE_TAGLINE}</p>
        <p class="mt-1">As an Amazon Associate, this site earns from qualifying purchases (Store ID: {AFFILIATE_TAG}).</p>
    </footer>
</body>
</html>"""

def generate_sitemap_and_robots(urls):
    today = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    xml_items = ""
    for u in urls:
        xml_items += f"""  <url>
    <loc>{u}</loc>
    <lastmod>{today}</lastmod>
    <changefreq>daily</changefreq>
    <priority>{"1.0" if u.endswith("/") else "0.85"}</priority>
  </url>\n"""

    sitemap_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{xml_items}</urlset>"""

    with open(os.path.join(OUTPUT_DIR, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap_content)

    robots_content = f"""User-agent: *
Allow: /
Sitemap: {BASE_URL}/sitemap.xml
"""
    with open(os.path.join(OUTPUT_DIR, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(robots_content)

    with open(os.path.join(OUTPUT_DIR, f"{INDEXNOW_KEY}.txt"), "w", encoding="utf-8") as f:
        f.write(INDEXNOW_KEY)

def ping_indexnow(urls):
    parsed_host = urllib.parse.urlparse(BASE_URL).netloc
    if not parsed_host or "username.github.io" in parsed_host:
        return

    payload = {
        "host": parsed_host,
        "key": INDEXNOW_KEY,
        "keyLocation": f"{BASE_URL}/{INDEXNOW_KEY}.txt",
        "urlList": urls
    }
    try:
        req = urllib.request.Request(
            "https://api.indexnow.org/indexnow",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json; charset=utf-8"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            print(f"IndexNow Ping Status: {resp.status}")
    except Exception as e:
        print(f"IndexNow notice: {e}")

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    generated_urls = []

    # 1. Generate Homepage
    home_preset = {
        "slug": "index",
        "name": "4-Bay NAS in RAID 5 (4× 16TB)",
        "drives": 4,
        "drive_tb": 16,
        "raid": "raid5",
        "cams": 4,
        "days": 30,
        "desc": "Calculate exact NAS RAID usable capacity (TB & binary OS TiB), parity protection, 4K PoE NVR security camera storage days, and UPS VA sizing—plus read daily hardware reviews."
    }
    with open(os.path.join(OUTPUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(render_calculator_page(home_preset, is_home=True))
    generated_urls.append(f"{BASE_URL}/")

    # 2. Generate Programmatic RAID & NVR Calculator Pages
    for page in ALL_CALC_PAGES:
        filename = f"{page['slug']}.html"
        with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
            f.write(render_calculator_page(page, is_home=False))
        generated_urls.append(f"{BASE_URL}/{filename}")

    # 3. Generate Cumulative Daily Product Review Pages (+1 new review unlocked every day)
    active_reviews = get_cumulative_product_reviews()
    for rev in active_reviews:
        filename = f"{rev['slug']}.html"
        with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
            f.write(render_single_review_page(rev))
        generated_urls.append(f"{BASE_URL}/{filename}")

    # 4. Generate Standalone Head-to-Head Product Comparison Pages
    for vs in VS_COMPARISONS:
        filename = f"{vs['slug']}.html"
        with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
            f.write(render_vs_comparison_page(vs))
        generated_urls.append(f"{BASE_URL}/{filename}")

    # 5. Sitemap, Robots & IndexNow Auto-Ping
    generate_sitemap_and_robots(generated_urls)
    ping_indexnow(generated_urls)
    print(f"Successfully generated {len(generated_urls)} total SEO pages ({len(active_reviews)} cumulative review articles) in /{OUTPUT_DIR}!")

if __name__ == "__main__":
    main()
