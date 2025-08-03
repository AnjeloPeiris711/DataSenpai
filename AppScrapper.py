import csv
import os
import time
from google_play_scraper import  app, Sort, reviews_all

class AppDetailsScraper:
    def __init__(self):
        self.scraped_data = []
    
    def scrape_app_details(self, package_name):
        """Scrape details for a single app"""
        try:
            print(f"🔄 Scraping: {package_name}")
            
            # Get app metadata
            result = app(package_name)
            
            app_name = result['title']
            downloads = result['installs']
            rating = result['score']
            description = result.get('description', '')
            screenshots = result['screenshots']  # You can increase number if needed

            # Create key features from available metadata
            key_features = '\n'.join(screenshots)
            
            # Get reviews (limit to avoid too much data)
            try:
                reviews = reviews_all(
                    package_name,
                    sleep_milliseconds=100,  # Small delay to be respectful
                    lang='en',
                    country='us',
                    sort=Sort.MOST_RELEVANT,
                    filter_score_with=None
                )
                
                # Separate good and bad reviews
                good_reviews = [r['content'] for r in reviews if r['score'] >= 4][:3]
                bad_reviews = [r['content'] for r in reviews if r['score'] <= 2][:3]
                
                # Join reviews as text
                good_text = '\n---\n'.join(good_reviews) if good_reviews else "No good reviews found"
                bad_text = '\n---\n'.join(bad_reviews) if bad_reviews else "No bad reviews found"
                
                print(f"✅ Found {len(reviews)} reviews for {app_name}")
                
            except Exception as e:
                print(f"⚠️  Could not fetch reviews for {package_name}: {e}")
                good_text = "Reviews not available"
                bad_text = "Reviews not available"
            
            # Store the data
            app_data = {
                'App': app_name,
                'Package': package_name,
                'Downloads': downloads,
                'Rating': rating,
                'Key Features': key_features,
                'Good (Pros)': good_text,
                'Bad (Cons)': bad_text
            }
            
            self.scraped_data.append(app_data)
            print(f"✅ Successfully scraped: {app_name}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error scraping {package_name}: {e}")
            return False
    
    def scrape_from_file(self, filename='app_ids.txt'):
        """Read app IDs from file and scrape each one"""
        if not os.path.exists(filename):
            print(f"❌ File {filename} not found!")
            return False
        
        with open(filename, 'r') as f:
            app_ids = [line.strip() for line in f.readlines() if line.strip()]
        
        print(f"📱 Found {len(app_ids)} apps to scrape")
        
        successful = 0
        for i, app_id in enumerate(app_ids, 1):
            print(f"\n[{i}/{len(app_ids)}] Processing: {app_id}")
            if self.scrape_app_details(app_id):
                successful += 1
            
            # Small delay between requests to be respectful
            time.sleep(1)
        
        print(f"\n🎉 Successfully scraped {successful}/{len(app_ids)} apps")
        
        # Save to CSV
        self.save_to_csv()
        return True
    
    def save_to_csv(self, filename='app_details.csv'):
        """Save all scraped data to CSV"""
        if not self.scraped_data:
            print("❌ No data to save!")
            return
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['App', 'Package', 'Downloads', 'Rating', 'Key Features', 'Good (Pros)', 'Bad (Cons)']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for app_data in self.scraped_data:
                writer.writerow(app_data)
        
        print(f"💾 Saved {len(self.scraped_data)} apps to {filename}")