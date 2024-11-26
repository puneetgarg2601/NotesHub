
def getEngagementRate(note):
    rate = ((note['upvotes'] + note['bookmark_count']) / note['view_count'] * 100) if note['view_count'] > 0 else 0
    rate = f'{rate:.3f}'[:-1]
    return rate

def getAvgTimePerView(note):
    rate = note['total_time_spent'] / note['view_count'] if note['view_count'] > 0 else 0
    rate = f'{rate:.3f}'[:-1]
    return rate

def getUpvoteRatio(note):
    rate = note['upvotes'] / (note['upvotes'] + note['downvotes']) if (note['upvotes'] + note['downvotes']) > 0 else 0
    rate = f'{rate:.3f}'[:-1]
    return rate