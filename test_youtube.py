from src.scraper import search_youtube


print("=" * 45)
print("SENTIMENT ANALYST - YOUTUBE API TEST")
print("=" * 45)

try:
    result = search_youtube(
        keyword="rupiah melemah",
        max_contents=3,
        max_comments=5,
        language="Indonesian"
    )

    print("\nVIDEO DITEMUKAN:", len(result["contents"]))
    print("KOMENTAR DIKUMPULKAN:", len(result["comments"]))

    print("\n--- DAFTAR VIDEO ---")

    for video in result["contents"]:
        print("\nJudul:", video["title"])
        print("Channel:", video["author"])
        print("URL:", video["content_url"])

    print("\n--- CONTOH KOMENTAR ---")

    for comment in result["comments"][:10]:
        print("\nPlatform:", comment["platform"])
        print("Video:", comment["content_title"])
        print("Akun:", comment["author"])
        print("Komentar:", comment["text"])

    if result["errors"]:
        print("\n--- VIDEO DENGAN ERROR ---")
        for error in result["errors"]:
            print(error["content_title"], error["error"])

    print("\nTES SELESAI.")

except Exception as error:
    print("\nTES GAGAL!")
    print("Penyebab:", error)