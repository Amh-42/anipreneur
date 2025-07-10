import re
import json
from datetime import datetime
from typing import List, Dict, Optional

class SEOUtils:
    """SEO utility functions for content optimization"""
    
    @staticmethod
    def generate_meta_description(content: str, max_length: int = 160) -> str:
        """Generate meta description from content"""
        # Remove HTML tags
        clean_content = re.sub(r'<[^>]+>', '', content)
        # Remove extra whitespace
        clean_content = re.sub(r'\s+', ' ', clean_content).strip()
        
        if len(clean_content) <= max_length:
            return clean_content
        
        # Truncate at word boundary
        words = clean_content[:max_length].split()
        if len(words) > 1:
            words.pop()  # Remove last incomplete word
        return ' '.join(words) + '...'
    
    @staticmethod
    def extract_keywords_from_title(title: str) -> List[str]:
        """Extract potential keywords from title"""
        # Remove common words and punctuation
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        words = re.findall(r'\b\w+\b', title.lower())
        keywords = [word for word in words if word not in stop_words and len(word) > 2]
        return keywords[:5]  # Return top 5 keywords
    
    @staticmethod
    def calculate_keyword_density(content: str, keyword: str) -> float:
        """Calculate keyword density in content"""
        clean_content = re.sub(r'<[^>]+>', '', content).lower()
        word_count = len(clean_content.split())
        keyword_count = clean_content.count(keyword.lower())
        
        if word_count == 0:
            return 0.0
        
        return (keyword_count / word_count) * 100
    
    @staticmethod
    def generate_schema_markup(post_data: Dict) -> str:
        """Generate JSON-LD schema markup for blog post"""
        schema = {
            "@context": "https://schema.org",
            "@type": "BlogPosting",
            "headline": post_data.get('title', ''),
            "description": post_data.get('meta_description', ''),
            "image": post_data.get('featured_image', ''),
            "author": {
                "@type": "Person",
                "name": post_data.get('author_name', 'Anipreneur')
            },
            "publisher": {
                "@type": "Organization",
                "name": "Anipreneur",
                "logo": {
                    "@type": "ImageObject",
                    "url": "https://anipreneur.com/static/images/logo.png"
                }
            },
            "datePublished": post_data.get('created_at', ''),
            "dateModified": post_data.get('updated_at', ''),
            "mainEntityOfPage": {
                "@type": "WebPage",
                "@id": post_data.get('canonical_url', '')
            }
        }
        
        return json.dumps(schema, indent=2)
    
    @staticmethod
    def seo_score_check(content: str, title: str, meta_description: str, focus_keyword: str) -> Dict:
        """Calculate SEO score for content"""
        score = 0
        issues = []
        suggestions = []
        
        # Title length check
        if len(title) < 30:
            issues.append("Title is too short (should be 30-60 characters)")
            score -= 10
        elif len(title) > 60:
            issues.append("Title is too long (should be 30-60 characters)")
            score -= 5
        else:
            score += 10
        
        # Meta description length check
        if len(meta_description) < 120:
            issues.append("Meta description is too short (should be 120-160 characters)")
            score -= 10
        elif len(meta_description) > 160:
            issues.append("Meta description is too long (should be 120-160 characters)")
            score -= 5
        else:
            score += 10
        
        # Focus keyword in title
        if focus_keyword.lower() in title.lower():
            score += 15
        else:
            issues.append("Focus keyword not found in title")
            score -= 15
        
        # Focus keyword in meta description
        if focus_keyword.lower() in meta_description.lower():
            score += 10
        else:
            issues.append("Focus keyword not found in meta description")
            score -= 10
        
        # Content length check
        word_count = len(content.split())
        if word_count < 300:
            issues.append("Content is too short (should be at least 300 words)")
            score -= 20
        elif word_count < 1000:
            suggestions.append("Consider adding more content (1000+ words for better ranking)")
            score += 5
        else:
            score += 15
        
        # Keyword density check
        density = SEOUtils.calculate_keyword_density(content, focus_keyword)
        if density < 0.5:
            issues.append("Keyword density too low (should be 0.5-2.5%)")
            score -= 10
        elif density > 2.5:
            issues.append("Keyword density too high (risk of keyword stuffing)")
            score -= 10
        else:
            score += 15
        
        # H1 check
        h1_count = content.count('<h1>')
        if h1_count == 0:
            issues.append("No H1 tag found")
            score -= 10
        elif h1_count > 1:
            issues.append("Multiple H1 tags found (should be only one)")
            score -= 5
        else:
            score += 10
        
        # Image alt tags check
        img_tags = re.findall(r'<img[^>]+>', content)
        img_with_alt = re.findall(r'<img[^>]+alt=["\'][^"\']+["\'][^>]*>', content)
        if img_tags and len(img_with_alt) < len(img_tags):
            issues.append("Some images missing alt tags")
            score -= 5
        
        # Internal links check
        internal_links = len(re.findall(r'href=["\'][^"\']*anipreneur[^"\']*["\']', content))
        if internal_links < 2:
            suggestions.append("Add more internal links (2-5 recommended)")
            score += 5
        
        return {
            'score': max(0, score),
            'issues': issues,
            'suggestions': suggestions,
            'word_count': word_count,
            'keyword_density': round(density, 2)
        }
    
    @staticmethod
    def generate_seo_title(title: str, focus_keyword: str, brand: str = "Anipreneur") -> str:
        """Generate SEO-optimized title"""
        # Ensure focus keyword is in title
        if focus_keyword.lower() not in title.lower():
            title = f"{title} - {focus_keyword}"
        
        # Add brand name if not present
        if brand.lower() not in title.lower():
            title = f"{title} - {brand}"
        
        # Ensure length is optimal
        if len(title) > 60:
            # Truncate at word boundary
            words = title[:57].split()
            if len(words) > 1:
                words.pop()
            title = ' '.join(words) + '...'
        
        return title
    
    @staticmethod
    def generate_seo_slug(title: str) -> str:
        """Generate SEO-friendly slug from title"""
        # Remove HTML tags
        clean_title = re.sub(r'<[^>]+>', '', title)
        # Convert to lowercase
        slug = clean_title.lower()
        # Replace special characters with hyphens
        slug = re.sub(r'[^\w\s-]', '', slug)
        # Replace spaces with hyphens
        slug = re.sub(r'[-\s]+', '-', slug)
        # Remove leading/trailing hyphens
        slug = slug.strip('-')
        
        return slug

# SEO Checklist Template
SEO_CHECKLIST = {
    "pre_publishing": [
        "✓ Keyword research completed",
        "✓ Primary keyword selected",
        "✓ Secondary keywords identified",
        "✓ Search intent analyzed",
        "✓ Competitor content reviewed",
        "✓ Content outline created"
    ],
    "content_creation": [
        "✓ Title optimized (30-60 characters)",
        "✓ Meta description written (120-160 characters)",
        "✓ Focus keyword in title and meta description",
        "✓ H1 tag contains primary keyword",
        "✓ Content length 1000+ words",
        "✓ Keyword density 0.5-2.5%",
        "✓ Internal links added (2-5)",
        "✓ External links to authoritative sources",
        "✓ Images with descriptive alt tags",
        "✓ Schema markup added"
    ],
    "technical_seo": [
        "✓ URL slug optimized",
        "✓ Canonical URL set",
        "✓ XML sitemap updated",
        "✓ Robots.txt configured",
        "✓ Page speed optimized",
        "✓ Mobile-friendly design",
        "✓ SSL certificate active"
    ],
    "post_publishing": [
        "✓ Google Search Console submission",
        "✓ Social media sharing",
        "✓ Internal linking from existing posts",
        "✓ Email newsletter promotion",
        "✓ Monitor search rankings",
        "✓ Track user engagement metrics"
    ]
} 