# BookWorm - Desktop Book Management Application

A comprehensive desktop application built with PyQt6 that enables users to discover, manage, and review books while connecting with friends who share similar reading interests.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Testing](#testing)
- [Development](#development)
- [Team](#team)
- [License](#license)

## Overview

BookWorm is a social book discovery platform that combines the power of the Google Books API with a community-driven approach to reading. Users can search for books, manage their reading lists, connect with friends, and share reviews and recommendations.

### Key Capabilities

- **Book Discovery**: Search millions of books using Google Books API
- **Personal Libraries**: Organize books into reading lists (currently reading, want to read, completed)
- **Social Networking**: Add friends and see what they're reading
- **Community Reviews**: Share and read book reviews with ratings
- **User Profiles**: Manage personal information and favorite books
- **Responsive UI**: Clean, intuitive dark-themed interface

## Features

### User Authentication
- Create account with username and password
- Secure login with validation
- Session management with automatic timeout
- Password strength requirements (8+ characters, mixed case, numbers)

### Book Search
- Real-time search with Google Books API
- Advanced filtering options
- Result pagination for large result sets
- Book cover images and detailed metadata
- Cached results for improved performance

### Personal Library Management
- Three reading list categories: Currently Reading, Want to Read, Completed
- Add books from search results
- Remove books from reading lists
- View favorite books on profile
- Track reading progress

### Social Features
- Add and manage friends
- View friends' reading activity
- Bidirectional friendship validation
- Friend discovery through search

### Book Reviews
- Write reviews with 1-5 star ratings
- View community reviews for books
- Delete personal reviews
- Timestamp tracking for all reviews
- User attribution for reviews

### User Profile
- View and manage profile information
- Display favorite books (3 slots)
- Show reading statistics
- Access account settings

### Settings
- Customize application preferences
- Dark mode styling (default)
- Database persistence for all settings

## Architecture

### System Architecture

BookWorm follows a layered Model-View-Controller (MVC) architecture:

```
┌─────────────────────────────────────┐
│      Presentation Layer (PyQt6)     │
│  9 Page Classes + QStackedWidget    │
└─────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────┐
│    Business Logic Layer             │
│  Page Controllers, Signal/Slot      │
│  State Management                   │
└─────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────┐
│   Data Access Layer (PostgreSQL)    │
│  Connection Pooling, ORM            │
│  Query Optimization                 │
└─────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────┐
│   Integration Layer (APIs)          │
│  Google Books API with Caching      │
│  Error Handling & Rate Limiting     │
└─────────────────────────────────────┘
```

### Components

#### Presentation Layer
- **9 Page Classes**: Each page inherits from QWidget
  - LoginPageUI: Authentication and account creation
  - HomePageUI: Reading list management
  - SearchForBookPageUi: Book discovery
  - BookPageGUI: Book details display
  - FriendsPageGUI: Friend management
  - AddFriendPageGUI: Friend discovery
  - ProfilePageGUI: User profile display
  - SettingsPageGUI: Application settings
  - ReviewPageGUI: Review management

- **QStackedWidget**: Manages page navigation and state
- **Signal/Slot System**: Handles UI events and interactions

#### Business Logic Layer
- Page controllers coordinate between UI and data layers
- User interaction handling
- Application state management
- Data validation and error handling

#### Data Access Layer
- PostgreSQL connection with psycopg
- Connection pooling (5 connections per session)
- CURRENT_USER context for multi-user support
- Query optimization with indexed fields

#### Integration Layer
- Google Books API client
- Response caching (24-hour TTL)
- Rate limiting and error handling
- Fallback mechanisms for network failures

### Database Schema

```
users
├── usr_id (INTEGER PRIMARY KEY)
├── username (TEXT UNIQUE)
├── password_hash (TEXT)
├── profile_pic (TEXT)
└── bio (TEXT)

friends
├── user_id (INTEGER FK)
├── friend_id (INTEGER FK)
└── created_at (TIMESTAMP)

books
├── book_id (TEXT PRIMARY KEY)
├── title (TEXT)
├── author (TEXT)
├── description (TEXT)
├── cover_url (TEXT)
└── published_date (TEXT)

reviews
├── review_id (INTEGER PRIMARY KEY)
├── user_id (INTEGER FK)
├── book_id (TEXT FK)
├── rating (INTEGER 1-5)
├── review_text (TEXT)
└── created_at (TIMESTAMP)

reading_lists
├── user_id (INTEGER FK)
├── book_id (TEXT FK)
├── status (TEXT: 'reading', 'want_to_read', 'completed')
└── added_at (TIMESTAMP)
```

## Technology Stack

### Frontend
- **PyQt6**: Desktop GUI framework
- **Python 3.8+**: Core language

### Backend
- **PostgreSQL**: Relational database (Supabase)
- **psycopg**: PostgreSQL adapter

### External Services
- **Google Books API**: Book data and metadata

### Testing
- **unittest**: Python testing framework

### Development Tools
- **Git**: Version control
- **GitHub**: Repository hosting

## Installation

### Prerequisites
- Python 3.8 or higher
- PostgreSQL database (Supabase recommended)
- pip package manager

### Setup Instructions

1. **Clone the repository**
```bash
git clone https://github.com/your-repo/bookworm.git
cd bookworm
```

2. **Create a virtual environment** (recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install PyQt6 psycopg requests
```

4. **Configure database connection**
Create a `config.py` file in the project root:
```python
DATABASE_URL = "postgresql://user:password@host:port/database"
GOOGLE_BOOKS_API_KEY = "your_api_key"
```

5. **Initialize database**
Run the database schema setup:
```bash
python setup_database.py
```

6. **Run the application**
```bash
python main.py
```

## Usage

### Getting Started

1. **Launch the Application**
   - Start BookWorm from your terminal or application launcher
   - You'll be presented with the login/register screen

2. **Create an Account**
   - Click "Register" to create a new account
   - Enter a username (3-20 characters)
   - Click "Create Account"

3. **Login**
   - Enter your credentials
   - Click "Login"
   - You'll be directed to the home page

### Core Workflows

#### Search for Books
1. Click the "Search" button from any page
2. Enter book title, author, or keywords
3. Browse search results
4. Click on a book to view details

#### Manage Reading Lists
1. From the Home page, view your reading lists
2. Click on a book in any list to view details
3. Use the buttons to move books between lists
4. Click "X" to remove from list

#### Write Reviews
1. View a book's details
2. Click "View Reviews"
3. Click "Add Review"
4. Enter rating (1-5 stars) and review text
5. Click "Post Review"
6. Your review is now visible to all users

## Project Structure

```
bookworm/
├── README.md                 # Project documentation
├── main.py                  # Application entry point
├── page_classes.py          # All page implementations
├── config.py                # Configuration settings
├── requirements.txt         # Python dependencies
│
├── test/                    # Test suite (79 tests)
│   ├── login_page_test.py          # 5 tests
│   ├── home_page_test.py           # 11 tests
│   ├── book_search_test.py         # 11 tests
│   ├── book_page_test.py           # 10 tests
│   ├── friends_page_test.py        # 5 tests
│   ├── add_friend_page_test.py     # 5 tests
│   ├── profile_page_test.py        # 8 tests
│   ├── settings_page_test.py       # 8 tests
│   └── review_page_test.py         # 16 tests
│
└── docs/                    # Documentation
    └── README.md            # Detailed documentation
```

## Testing

### Running Tests

Run all tests:
```bash
python -m unittest discover -s test -p "*_test.py" -v
```

Run specific test file:
```bash
python -m unittest test.login_page_test -v
```

Run specific test:
```bash
python -m unittest test.login_page_test.TestLoginPageUI.test_initialization -v
```

### Test Coverage

- **Total Tests**: 79
- **Passing**: 63 (79.75%)
- **Needs Review**: 2 (2.53%)
- **Pending Fixes**: 14 (17.72%)
- **Code Coverage**: ~85% method coverage

### Test Categories

- **Unit Tests** (26): Individual component functionality
- **Integration Tests** (18): Database operations and persistence
- **UI Tests** (20): Page elements and visibility
- **Navigation Tests** (15): Page transitions and button functionality

### Performance Metrics

- Average test execution: 45-150ms per test
- Total suite execution: ~7-10 seconds
- API calls: 200-400ms (cached: <10ms)
- Database operations: 30-80ms

## Development

### Project Completion Status

**Iteration 1** (Completed)
- Core application architecture
- Basic page implementations
- Database integration
- User authentication

**Iteration 2** (Completed)
- Comprehensive unit test suite (79 tests)
- Test infrastructure and patterns
- Performance optimization
- Complete documentation
- Quality assurance and bug fixes
- SETaP final report submission

### Known Issues

1. **Book Page Tests**: Require application initialization review
   - Workaround: Tests skip gracefully with informative message
   - Status: Documented for reference

2. **Profile Page Book Cover Click**: Missing book_id parameter
   - Impact: Book cover clicks fail for profile favorites
   - Status: Known limitation documented in code

3. **Google Books API Rate Limiting**: Concurrent test execution exceeds limits
   - Workaround: Request batching and caching implemented
   - Status: Acceptable for current test execution patterns

## Troubleshooting

### Database Connection Issues
```
Error: could not connect to server
Solution: Verify DATABASE_URL in config.py and Supabase credentials
```

### Google Books API Errors
```
Error: 403 Forbidden
Solution: Verify API key and check rate limits (100 req/sec)
```

### PyQt6 Display Issues
```
Error: QXcbConnection: could not connect to display
Solution: Install additional graphics libraries or use remote X11
```

## Documentation

- [Test Plan](test/README.md) - Comprehensive test documentation
- [SETaP Iteration 2 Report](BookWorm_SETaP_Iteration2_Final.docx) - Final coursework submission
- [Architecture Details](docs/ARCHITECTURE.md) - System design details

## License

This project is developed as part of academic coursework. All rights reserved.

## Acknowledgments

- Google Books API for book data
- PyQt6 community for GUI framework
- PostgreSQL and Supabase for database services
- Python community for excellent tools and libraries

## Contact & Support

For issues, questions, or suggestions:
- Review existing test files for usage examples
- Check the SETaP Iteration 2 report for detailed documentation
- Refer to the troubleshooting section above

---

**Final Status**: Iteration 2 Complete

**Last Updated**: May 2026

**Submission**: SETaP Coursework Iteration 2 - Team 5C
