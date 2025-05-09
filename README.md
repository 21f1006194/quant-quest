# quant-quest
A flagship event by Quantix, IITM, at Paradox'25; where participants apply statistics, mathematics, risk management and programming knowledge to solve puzzles (games).

## Quick Setup Guide

### Prerequisites
- Docker
- Docker Compose

### Development Setup
1. Clone the repository:
```bash
git clone https://github.com/21f1006194/quant-quest.git
cd quant-quest
```

2. Build and start development containers:
```bash
./compose.sh dev build
./compose.sh dev up
```

NOTE: The code files are mounted as volumes in the containers, so any changes to the code will be reflected immediately, no need to rebuild the containers.
The application will be available at:
- Frontend: http://localhost
- Backend API: http://localhost:5000

### Production Setup
1. Create `.env.prod` file in the root directory (refer to `.env.template` for required variables)

2. Build and start production containers:
```bash
./compose.sh prod build
./compose.sh prod up -d
```
