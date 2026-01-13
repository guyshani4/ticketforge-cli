# TicketForge CLI Integration

## Overview
A Python-based CLI tool to manage project tickets, developed as part of a technical assignment.

## Personal Reflection & Learning Process
This was my first experience with an integration project that required reverse-engineering an undocumented API. 
Throughout the assignment, I focused on:
- Learning how to utilize Browser DevTools (Network & Console) to intercept and analyze live traffic.
- Understanding the implementation of Basic Auth and how to handle it via Python's `requests` library.
- Discovering and adapting to modern web architectures like Next.js and React Server Components (RSC).

While the server enforced strict protections, I used this as an opportunity to experiment with header emulation and fallback mechanisms, treating the challenge as a learning milestone.

## Setup & Usage
1. `pip install -r requirements.txt`
2. `python3 main.py setup <Base64_Token>`
3. `python3 main.py list`

## Reverse Engineering & Technical Challenges
Throughout the development, I performed deep inspection of network traffic:
- **Authentication**: Identified `Basic Auth` requirement from 401 response headers.
- **404 Challenges**: Attempted to access several inferred endpoints (`/api/tickets`, `/api/mine`). 
- **Findings**: The application uses Next.js with React Server Components (RSC). The server appears to validate requests against browser-specific attributes, returning 404/HTML when accessed via standard HTTP clients.
- **Mitigation**: Implemented full Header emulation (User-Agent, Referer) to attempt bypass, though the server remains restrictive.

During the reverse engineering process, I identified a discrepancy between browser-based requests and CLI-based requests. While the browser successfully fetches data from /api/mine, the server implementation for this specific assignment deployment appears to enforce strict header validation or use React Server Components (RSC) that return HTML/404 when browser-specific headers are missing. To address this, I implemented a robust header emulation strategy and a fallback mechanism to test multiple inferred endpoints discovered via the Network tab.

## AI Disclosure
I utilized AI tools (Gemini/ChatGPT) to assist with the following:
- **Reverse Engineering**: Decoding the 401 Unauthorized error to identify the Basic Auth requirement.
- **Network Analysis**: Interpreting Chrome DevTools Network traffic to locate potential API endpoints and understand RSC (React Server Components) headers.
- **Code Architecture**: Structuring the Python CLI boilerplate, including the configuration setup and error handling logic.
- **Learning**: Since this was my first integration project of this type, I used AI as a learning partner to quickly grasp concepts like Base64 encoding and HTTP header emulation.
