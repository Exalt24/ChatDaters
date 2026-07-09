# ChatDaters

A dating platform with Tinder-style swipe matching, real-time match notifications, and in-app messaging. Built solo in a three-day sprint during my Full Stack Developer internship at ChatGenie.PH (Techstars '23, July 2024).

Users swipe through profiles, get matched when interest is mutual, and chat in real time once matched.

## Features

- **Swipe matching** — Tinder-style like/pass with mutual-match detection.
- **Real-time notifications** — new matches and messages arrive live over WebSockets.
- **In-app messaging** — chat threads open automatically between matched users.

## Tech Stack

- **Backend:** Ruby on Rails API, with Action Cable for WebSocket messaging
- **Frontend:** Vue 3, Vite, Tailwind CSS, Apollo client

## Structure

This is a monorepo merged from the two original repositories (with full git history preserved):

```
backend/    Ruby on Rails API + Action Cable
frontend/   Vue 3 + Vite + Tailwind single-page app
```

## Getting Started

**Backend**

```bash
cd backend
bundle install
rails db:create db:migrate
rails server
```

**Frontend**

```bash
cd frontend
npm install
npm run dev
```

## Context

One of two applications I shipped solo during my ChatGenie.PH internship (the other is [ChatHotel](https://github.com/Exalt24/ChatHotel)), each built in a compressed three-day sprint.
