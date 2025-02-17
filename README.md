# WatchTower

## To run the frontend 
- navigate to ../frontend directory in your machine
- npm install
- npm install tailwindcss @tailwindcss/vite
- npm run dev

## To start frontend development
- download `ES7 React/Redux/GraphQL/React-Native snippets` in your VS code.
- create .js file and type `rcfe`.

## Backend intro video
- `https://www.youtube.com/watch?v=cJveiktaOSQ&t=486s&ab_channel=PedroTech`

## Backend Structure

```
/backend/               # Main project directory
├── backend/           # Project configuration directory
│   ├── settings.py    # Project settings
│   ├── urls.py       # Main URL configuration
│   ├── wsgi.py       # WSGI configuration
│   └── asgi.py       # ASGI configuration
│
├── api/              # API application
│   ├── views.py      # API endpoint logic
│   ├── urls.py       # API route definitions
│   └── serializers.py # Data serialization
│
└── watchtower/       # Main application
    ├── models.py     # Database models
    ├── admin.py      # Admin interface config
    ├── views.py      # View logic
    └── migrations/   # Database migrations
```

- To preview api endpoints configure your .env file, enter `/backend` and run `python manage.py runserver`.

# WatchTower Git Workflow Guide

## Initial Setup

1. **Clone the main repository**
```bash
git clone https://github.com/CSCI-321-WatchTower/WatchTower.git
cd WatchTower
```

2. **Add your fork as a remote**
```bash
git remote add origin https://github.com/YourUsername/WatchTower.git
git remote add upstream https://github.com/CSCI-321-WatchTower/WatchTower.git
```

## Daily Workflow

1. **Update your local main branch**
```bash
git checkout main
git fetch upstream
git rebase upstream/main
```

2. **Create a feature branch**
```bash
git checkout -b feature/your-feature-name
```

3. **Make changes and commit**
```bash
git add .
git commit -m "feat: your meaningful commit message"
```

## Commit Message Format
```
type: subject

body (optional)

footer (optional)
```

Types:
- feat: new feature
- fix: bug fix
- docs: documentation
- style: formatting
- refactor: code restructuring
- test: adding tests
- chore: maintenance

## Handling Updates

1. **Update feature branch with main**
```bash
git checkout feature/your-feature-name
git fetch upstream
git rebase upstream/main
```

2. **If conflicts occur**
```bash
# Resolve conflicts in VS Code
git add .
git rebase --continue
```

3. **If rebase gets messy**
```bash
git rebase --abort
git reset --hard origin/feature/your-feature-name
```

## Push Changes

1. **Push to your fork**
```bash
git push origin feature/your-feature-name
```

2. **If push is rejected**
```bash
git push --force-with-lease origin feature/your-feature-name
```

## Clean Up

1. **Clean up local branches**
```bash
git fetch -p
git branch -vv | findstr ": gone]" | foreach { git branch -D $_.Split()[0] }
```

2. **Reset to clean state**
```bash
git reset --hard upstream/main
git clean -fd
```

## Project-Specific Setup

1. **Environment setup**
```bash
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
```

2. **Configure environment**
```bash
copy .env.example .env
# Edit .env with your settings
```

## Git Configuration

```bash
# Configure Git for rebasing
git config pull.rebase true
git config branch.main.rebase true

# Set VS Code as default editor
git config --global core.editor "code --wait"
```

## Troubleshooting

1. **Stuck in rebase**
```bash
# Check status
git status

# Choose one:
git rebase --continue
git rebase --abort
git rebase --skip
```

2. **Reset to clean state**
```bash
# Create backup
git checkout -b backup-branch

# Reset main
git checkout main
git reset --hard upstream/main
```

## Best Practices

1. **Before starting work**
```bash
git checkout main
git fetch upstream
git rebase upstream/main
git checkout -b feature/new-feature
```

2. **Before pushing changes**
```bash
git fetch upstream
git rebase upstream/main
git push origin feature/new-feature
```

3. **Keep commits atomic**
- One logical change per commit
- Use meaningful commit messages
- Reference issues in commits

4. **Branch naming**
- feature/feature-name
- fix/bug-name
- docs/documentation-update
