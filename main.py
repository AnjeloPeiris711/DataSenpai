from google_play_scraper import search
import json
from AppScrapper import AppDetailsScraper

class SearchPlayStoreApps:
    def __init__(self, keywords):
        print(f"🔍 Searching for apps with keywords: '{keywords}'")
        
        # Search for apps
        result = search(
            keywords,
            lang="en",
            country="us",
        )
        
        # Filter and save app IDs based on genre
        self.filtered_app_ids = []
        excluded_genres = ["casual", "simulation"]  # genres to exclude (case-insensitive)

        for app_data in result:
            # Get the genre from the app data
            genre = app_data.get('genre', '').lower()
        
            # Check if genre is not in excluded list
            if genre not in excluded_genres:
                app_id = app_data.get('appId')
                if app_id:
                    self.filtered_app_ids.append({
                        'appId': app_id,
                        'title': app_data.get('title', ''),
                        'genre': app_data.get('genre', ''),
                        'developer': app_data.get('developer', '')
                    })
                    print(f"✅ Added: {app_id} - {app_data.get('title', '')} (Genre: {app_data.get('genre', '')})")
            else:
                print(f"❌ Excluded: {app_data.get('appId', '')} - {app_data.get('title', '')} (Genre: {app_data.get('genre', '')})")

        print(f"\n📊 Total apps found: {len(result)}")
        print(f"📊 Apps after filtering: {len(self.filtered_app_ids)}")

        # Save filtered app IDs to a file
        with open('filtered_app_ids.json', 'w') as f:
            json.dump(self.filtered_app_ids, f, indent=2)

        # Save just the app IDs to a text file (one per line)
        with open('app_ids.txt', 'w') as f:
            for app_data in self.filtered_app_ids:
                f.write(f"{app_data['appId']}\n")

        print(f"💾 Filtered app data saved to 'filtered_app_ids.json'")
        print(f"💾 App IDs saved to 'app_ids.txt'")


def main():
    print("""
    ( • ) ( • )ԅ(‾⌣‾ԅ)
        DataSenpai
      PlayStore Scraper Tool
    ========================
    """)
    
    while True:
        print("\nChoose an option:")
        print("1. Search for apps by keywords")
        print("2. Scrape details from saved app IDs")
        print("3. Do both (search then scrape)")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            keywords = input("Enter keywords to search: ").strip()
            if keywords:
                searcher = SearchPlayStoreApps(keywords)
                print(f"\n✅ Search completed! Found {len(searcher.filtered_app_ids)} apps")
            else:
                print("❌ Please enter valid keywords!")
        
        elif choice == '2':
            scraper = AppDetailsScraper()
            if scraper.scrape_from_file():
                print("\n✅ Scraping completed!")
            else:
                print("\n❌ Scraping failed! Make sure you have run the search first.")
        
        elif choice == '3':
            keywords = input("Enter keywords to search: ").strip()
            if keywords:
                # First search
                print("\n=== STEP 1: SEARCHING ===")
                searcher = SearchPlayStoreApps(keywords)
                
                if searcher.filtered_app_ids:
                    print(f"\n✅ Search completed! Found {len(searcher.filtered_app_ids)} apps")
                    
                    # Ask user if they want to proceed with scraping
                    proceed = input(f"\nDo you want to scrape details for these {len(searcher.filtered_app_ids)} apps? (y/n): ").strip().lower()
                    
                    if proceed == 'y':
                        print("\n=== STEP 2: SCRAPING DETAILS ===")
                        scraper = AppDetailsScraper()
                        if scraper.scrape_from_file():
                            print("\n🎉 Complete process finished!")
                        else:
                            print("\n❌ Scraping failed!")
                    else:
                        print("👍 Search results saved. You can scrape later using option 2.")
                else:
                    print("\n❌ No apps found with those keywords!")
            else:
                print("❌ Please enter valid keywords!")
        
        elif choice == '4':
            print("👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice! Please enter 1, 2, 3, or 4.")

if __name__ == "__main__":
    main()