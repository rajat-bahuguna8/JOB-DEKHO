"""
Intelligent Job Matching Algorithm for JOB DEKHO
Matches students with jobs based on CGPA, branch, and skills
"""

def calculate_match_score(student, job):
    """
    Calculate match score between student and job
    Returns (score, details_dict)
    Score is out of 100
    """
    score = 0
    details = {
        'cgpa_match': False,
        'branch_match': False,
        'skills_match': [],
        'cgpa_score': 0,
        'branch_score': 0,
        'skills_score': 0
    }
    
    # CGPA Matching (40 points)
    if student.cgpa >= job.min_cgpa:
        details['cgpa_match'] = True
        # Extra points for higher CGPA
        cgpa_excess = student.cgpa - job.min_cgpa
        details['cgpa_score'] = min(40, 30 + (cgpa_excess * 5))
        score += details['cgpa_score']
    else:
        return 0, details  # Automatic rejection if CGPA doesn't meet minimum
    
    # Branch Matching (30 points)
    if job.required_branch.lower() in ['any', 'all branches']:
        details['branch_match'] = True
        details['branch_score'] = 30
        score += 30
    elif student.branch.lower() == job.required_branch.lower():
        details['branch_match'] = True
        details['branch_score'] = 30
        score += 30
    else:
        return 0, details  # Automatic rejection if branch doesn't match
    
    # Skills Matching (30 points)
    if job.required_skills:
        job_skills = set(skill.strip().lower() for skill in job.required_skills.split(','))
        student_skills = set(skill.strip().lower() for skill in student.skills.split(',')) if student.skills else set()
        
        matched_skills = job_skills.intersection(student_skills)
        details['skills_match'] = list(matched_skills)
        
        if matched_skills:
            skill_match_ratio = len(matched_skills) / len(job_skills)
            details['skills_score'] = skill_match_ratio * 30
            score += details['skills_score']
        else:
            return 0, details  # No matching skills
    
    return round(score, 2), details

def get_recommended_jobs(student, all_jobs, min_match_score=60):
    """
    Get recommended jobs for a student
    Returns list of (job, score, details) tuples, sorted by score
    """
    recommendations = []
    
    for job in all_jobs:
        if not job.is_active:
            continue
        
        score, details = calculate_match_score(student, job)
        
        if score >= min_match_score:
            recommendations.append((job, score, details))
    
    # Sort by score (descending)
    recommendations.sort(key=lambda x: x[1], reverse=True)
    
    return recommendations

def auto_shortlist_status(score):
    """
    Determine application status based on match score
    """
    if score >= 90:
        return 'Shortlisted'  # Excellent match
    elif score >= 75:
        return 'Applied'  # Good match, awaiting review
    else:
        return 'Applied'  # Meets minimum requirements
