import webbrowser
import datetime
import os

def trigger_police_alert(location, camera_id, activity_type):
    # 1. Capture Details (Day 6 Requirements)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report_name = f"ALERT_{camera_id}_{datetime.datetime.now().strftime('%H%M%S')}.html"
    
    # 2. Console Notification (Immediate Alert)
    print("\n" + "!"*40)
    print(f" ALERT: {activity_type} DETECTED!")
    print(f"LOCATION: {location} | CAMERA: {camera_id}")
    print(f"TIME: {timestamp}")
    print("!"*40 + "\n")

    # 3. Generate Secure Web Report (Dashboard Integration)
    # This creates a standalone file for the police to view
    report_content = f"""
    <html>
    <body style="font-family: Arial; background: #f8d7da; color: #721c24; padding: 20px;">
        <h1> Official Police Alert</h1>
        <hr>
        <p><b>Activity:</b> {activity_type}</p>
        <p><b>Timestamp:</b> {timestamp}</p>
        <p><b>Location:</b> {location}</p>
        <p><b>Device:</b> {camera_id}</p>
        <div style="border: 2px solid black; background: #eee; width: 300px; height: 200px; display: flex; align-items: center; justify-content: center;">
            [Snapshot/Video Clip Placeholder]
        </div>
        <p><i>Status: Automated detection from  Monitoring System</i></p>
    </body>
    </html>
    """
    
    with open(report_name, "w",encoding="utf-8") as f:
        f.write(report_content)
        webbrowser.open(report_name)
    
    print(f" Secure report generated: {report_name}")

# --- SIMULATION ---
# This part mimics your 'Activity Recognition Model' detecting a threat
if __name__ == "__main__":
    print("System Monitoring Active...")
    # Simulate a detection event
    trigger_police_alert("Main Lobby", "CAM-04", "Unauthorized Entry - High Risk")