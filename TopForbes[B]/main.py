import crawler
import functions

if __name__ == "__main__":
    crawler.start_crawling()
    print(f"Top 10 youngest persons: {functions.get_youngest(10)}")
    print(f"Citizenship: {functions.get_citizenship('United States')}")
    print(f"Top 10 highest score: {functions.get_highest_score(10)}")
