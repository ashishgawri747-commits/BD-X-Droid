import subprocess, cv2, time, base64
from openai import OpenAI

client = OpenAI(api_key="")

def grab_frame():
    subprocess.run(["libcamera-jpeg", "-o", "/tmp/pic.jpg", "--width", "640", "--height", "480", "-n"], check=True)
    return cv2.imread("/tmp/pic.jpg")

def describe_image(frame):
    _, buffer = cv2.imencode(".jpg", frame)
    b64 = base64.b64encode(buffer).decode("utf-8")
    r = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{
            "role":"user",
            "content":[
                {"type":"text","text":"Briefly describe what is visible in this image."},
                {"type":"image_url","image_url":{"url":f"data:image/jpeg;base64,{b64}"}}
            ]
        }]
    )
    return r.choices[0].message.content.strip()

def main():
    observations=[]
    print("?? Starting 10-second observation...")
    for i in range(10):
        frame = grab_frame()
        if frame is None:
            print("?? Frame capture failed.")
            continue
        desc = describe_image(frame)
        observations.append(desc)
        print(f"[{i+1}/10] {desc}")
        time.sleep(1)

    summary_prompt = "Summarize these 10 descriptions:\n" + "\n".join(f"- {d}" for d in observations)
    summary = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":summary_prompt}]
    ).choices[0].message.content.strip()
    print("\n=== ?? FINAL SCENE SUMMARY ===")
    print(summary)

if __name__=="__main__":
    main()
