import csv
from statistics import mean

FEATURES = [
    "popularity",
    "danceability",
    "energy",
    "tempo",
    "valence",
]

def load_hiphop_rows(csv_path):
    with open(csv_path, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # the dataset may include a BOM in the header
            genre = row.get("genre") or row.get("\ufeffgenre")
            if genre == "Hip-Hop":
                yield row


def compute_feature_means(rows):
    stats = {f: [] for f in FEATURES}
    for row in rows:
        for f in FEATURES:
            val = row.get(f)
            if val:
                stats[f].append(float(val))
    return {f: round(mean(values), 2) for f, values in stats.items() if values}


def most_popular(rows, n=5):
    sorted_rows = sorted(rows, key=lambda r: int(r.get("popularity", 0)), reverse=True)
    top = []
    for r in sorted_rows[:n]:
        track = r.get("track_name", "")
        artist = r.get("artist_name", "")
        pop = r.get("popularity", 0)
        top.append(f"{track} - {artist} (Popularity: {pop})")
    return top


def main():
    csv_path = "data/SpotifyFeatures.csv"
    hiphop_rows = list(load_hiphop_rows(csv_path))
    means = compute_feature_means(hiphop_rows)
    print("Averages for Hip-Hop tracks:")
    for f in FEATURES:
        print(f, means.get(f))
    print()
    print("Top Hip-Hop tracks:")
    for line in most_popular(hiphop_rows):
        print(line)


if __name__ == "__main__":
    main()
