## Youtube Video Downloader v2

This project aims to develop a system that automatically sends email notifications when selected YouTube channels upload a new video or go live, and downloads the recorded video after the live session ends. The system uses the **YouTube Data API** to monitor channel statuses and implements core functionalities using **Python**. Data is managed via an **SQLite** database.

### Why an OOP version?

While the functional version works fine, it can become harder to maintain as the project grows.  
Refactoring it into an object-oriented structure helps demonstrate:

- Code organization
- Separation of concerns
- Reusability
- Scalability

It’s also a great exercise to show flexibility in thinking as a developer.

### Features

* **YouTube API Integration:** Monitor the video and live broadcast status of selected channels.
* **Email Notifications:** Automatically send email alerts when new videos or live sessions are detected.
* **Video Downloading:** Automatically download the recorded video after a live broadcast ends.
* **Data Management:** Store and manage project data using SQLite.

### Installation
1. Clone the repository
```
git clone https://github.com/bahadirbor/video_downloader.git
cd video_downloader
```

2. Install the requirements
```
pip install -r requirements.txt
```

3. Configure API keys and Settings
* Store your YouTube API key and other sensitive information in a ```.env``` file.


