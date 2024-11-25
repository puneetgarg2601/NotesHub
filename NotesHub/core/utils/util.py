
def getEngagementRate(note):
    return ((note.upvotes + note.bookmark_count) / note.view_count * 100) if note.view_count > 0 else 0

def getAvgTimePerView(note):
    return note.total_time_spent / note.view_count if note.view_count > 0 else 0