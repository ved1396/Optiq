import logging

from db.database import get_db_connection

logger = logging.getLogger(__name__)


def log_query(
    *,
    query: str,
    route: str,
    response: str,
    latency_ms: float,
    estimated_cost: float,
    estimated_energy: float,
    confidence_score: float,
    classifier_label: str,
    heuristic_route: str | None,
) -> int:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO queries (
                query, route, response, latency_ms, estimated_cost, estimated_energy,
                confidence_score, classifier_label, heuristic_route
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                query,
                route,
                response,
                latency_ms,
                estimated_cost,
                estimated_energy,
                confidence_score,
                classifier_label,
                heuristic_route,
            ),
        )
        query_id = cursor.lastrowid
        cursor.execute(
            """
            INSERT INTO analytics (
                query_id, query, route, latency_ms, estimated_cost, estimated_energy, confidence_score
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                query_id,
                query,
                route,
                latency_ms,
                estimated_cost,
                estimated_energy,
                confidence_score,
            ),
        )
        conn.commit()
    logger.info("Logged query %s to analytics", query_id)
    return int(query_id)


def log_feedback(query_id: int, rating: int, comments: str | None, correct_route: str | None) -> None:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            UPDATE analytics
            SET feedback_rating = ?, feedback_comments = ?, correct_route = ?
            WHERE query_id = ?
            """,
            (rating, comments, correct_route, query_id),
        )
        if cursor.rowcount == 0:
            raise ValueError(f"Query id {query_id} was not found in analytics.")
        conn.commit()
