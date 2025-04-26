
from get_subs import get_sub_count
from generate_thumbnail import generate_thumbnail
from upload_thumbnail import upload_thumbnail

VIDEO_ID = "NDc6WR83RrM"

def main():
    subs = get_sub_count()
    print(f"Current subs: {subs}")

    generate_thumbnail(subs)
    upload_thumbnail(VIDEO_ID, "thumbnail.jpg")

if __name__ == "__main__":
    main()

