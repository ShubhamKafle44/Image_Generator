# AI Image Generation Platform

## Overview
This project is an AI-powered system that generates realistic images using both text prompts and input images. The goal is to keep the structure of the original image while applying the style and meaning described in the text prompt.

## Features
- **Image + Text Generation:** Produces high‑quality images using both image structure and text guidance.
- **ControlNet + Stable Diffusion:** Ensures the generated output follows the edges and depth of the input image.
- **User Authentication:** Each user can securely access their own history and generated images.
- **Dashboard:** Shows past prompts, generated images, and metadata.
- **Cloud Storage:** Stores user data and results using PostgreSQL and S3.
- **Optimized Performance:** GPU inference is tuned for fast, low‑latency responses.

## Tech Stack
- **Backend:** FastAPI (Python)
- **AI Models:** ControlNet, Stable Diffusion
- **Frontend:** React
- **Database:** PostgreSQL
- **Storage:** AWS S3
- **Authentication:** Clerk
- **Monitoring:** CloudWatch

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/your-repo.git
   ```
2. Install backend dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Install frontend dependencies:
   ```bash
   npm install
   ```
4. Set environment variables for:
   - Database
   - S3
   - Clerk
   - Model paths

5. Start the backend:
   ```bash
   uvicorn main:app --reload
   ```
6. Start the frontend:
   ```bash
   npm start
   ```

## Usage
1. Log in using Clerk.
2. Upload an image and enter a text prompt.
3. The system generates an image that follows the original structure.
4. View your history from the dashboard.

## Future Improvements
- Improve prompt understanding.
- Enhance generation quality.
- Add more ControlNet types.
- Improve UI/UX performance.

## License
MIT License

## Author
Shubham Kafle

