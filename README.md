# Smart Campus Queue Management System

> A digital queue management platform designed to reduce waiting time at campus service counters through token-based queue tracking, estimated waiting time, administration tools, and analytics.

---

## Overview

The **Smart Campus Queue Management System** is a Python and Streamlit-based application that digitizes traditional campus queues.

Students can join a queue, receive a digital token, monitor their queue position, and view an estimated waiting time instead of standing in a physical queue.

Administrators can manage queues, call the next student, complete services, monitor counters, and analyze queue activity.

---

## Key Features

### Student Portal

- Student registration and login
- Select campus service
- Generate digital queue token
- View current token
- Track queue position
- Estimated waiting time
- Queue status updates

### Admin Dashboard

- Secure administrator login
- View active queues
- Call next student
- Manage queue status
- Complete service requests
- Monitor counters
- View queue statistics

### Digital Display

- Current token display
- Next tokens in queue
- Live queue information
- Designed for display on a campus screen

### Analytics

- Queue statistics
- Service-wise analysis
- Waiting-time analysis
- Visual data representation
- Historical queue information

### Reports

- Generate queue reports
- Export data
- Analyze service performance
- Review queue activity

---

## Why This Project?

Traditional campus counters often create long physical queues.

Students may spend unnecessary time waiting for:

- Fees
- Library
- Stationery
- Administrative services
- Other campus facilities

This project converts the physical queue into a **digital queue**, allowing students to spend their waiting time elsewhere while monitoring their position through the application.

---

## System Workflow

```text
Student
   |
   v
Login / Register
   |
   v
Select Service
   |
   v
Generate Token
   |
   v
Join Digital Queue
   |
   v
Track Queue Position
   |
   v
Estimated Waiting Time
   |
   v
Service Completed
##2. Author

### Divakar

Computer Science Student | Python Developer | Data Analytics & AI/ML Enthusiast

I build practical software and data-driven projects focused on solving real-world problems.

**GitHub:** https://github.com/Divakar10-ai
### 3. Analytics Module

Provides queue statistics, service-wise analysis, waiting-time information, and data visualization to help understand campus queue activity and service performance.

### 4. Reports Module

Provides queue reports, data exports, service performance information, and historical queue activity for administrators.

### 5. Prediction Module

Used for queue and waiting-time related calculations to provide students with an estimated waiting time.

---

## Database

The application uses **SQLite** for local data storage. The system maintains information related to students, administrators, queue tokens, services, queue status, waiting-time information, and service statistics. Local database files are intentionally excluded from Git using `.gitignore`.

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Divakar10-ai/Smart-Campus-Queue-Management.git

