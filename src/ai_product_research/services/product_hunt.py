from dataclasses import dataclass
from datetime import datetime
import httpx
import logging
from ai_product_research.domain import ProductHuntPost

log = logging.getLogger(__name__)

@dataclass
class ProductHuntService:
    access_token: str

    async def get_posts(self, posted_after: datetime, posted_before: datetime, limit: int = 20) -> list[ProductHuntPost]:
        """Get Product Hunt posts for a specific time range.

        Args:
            posted_after: Start datetime for filtering posts
            posted_before: End datetime for filtering posts
            limit: Maximum number of posts to retrieve (default: 50)

        Returns:
            List of ProductHuntPost objects for the specified time range
        """
        url = "https://api.producthunt.com/v2/api/graphql"

        query = """
        query GetPosts($postedAfter: DateTime!, $postedBefore: DateTime!, $limit: Int!) {
            posts(order: VOTES, postedAfter: $postedAfter, postedBefore: $postedBefore, first: $limit) {
                edges {
                    node {
                        id
                        name
                        tagline
                        description
                        votesCount
                        url
                        website
                        thumbnail {
                            url
                        }
                        topics {
                            edges {
                                node {
                                    name
                                }
                            }
                        }
                    }
                }
            }
        }
        """

        # Product Hunt expects ISO format datetime strings
        posted_after_str = posted_after.isoformat() + "Z" if not posted_after.tzinfo else posted_after.isoformat()
        posted_before_str = posted_before.isoformat() + "Z" if not posted_before.tzinfo else posted_before.isoformat()

        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

        payload = {
            "query": query,
            "variables": {
                "postedAfter": posted_after_str,
                "postedBefore": posted_before_str,
                "limit": limit,
            }
        }

        async with httpx.AsyncClient() as client:
            log.info(f"Fetching Product Hunt posts from {posted_after} to {posted_before}")
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()

            data = response.json()

            if "errors" in data:
                log.error(f"Product Hunt API errors: {data['errors']}")
                raise Exception(f"Product Hunt API error: {data['errors']}")

            edges = data.get("data", {}).get("posts", {}).get("edges", [])
            log.info(f"Retrieved {len(edges)} posts")

            # Convert raw dict data to ProductHuntPost models
            posts = []
            for edge in edges:
                node = edge["node"]
                post = ProductHuntPost(
                    id=node["id"],
                    name=node["name"],
                    tagline=node["tagline"],
                    description=node["description"],
                    votesCount=node["votesCount"],
                    url=node["url"],
                    website=node["website"],
                    thumbnail_url=node.get("thumbnail", {}).get("url") if node.get("thumbnail") else None,
                    topics=[edge["node"]["name"] for edge in node.get("topics", {}).get("edges", [])]
                )
                posts.append(post)

            return posts
