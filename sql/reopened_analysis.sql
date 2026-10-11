WITH reopen_by_type AS (

    SELECT
        Request_Type,

        ROUND(
            AVG(
                CASE
                    WHEN Reopened = 0
                    THEN SLA_Breached
                END
            ) * 100,
            2
        ) AS No_Reopen_SLA_Rate,

        ROUND(
            AVG(
                CASE
                    WHEN Reopened = 1
                    THEN SLA_Breached
                END
            ) * 100,
            2
        ) AS Reopened_SLA_Rate

    FROM business_requests

    GROUP BY Request_Type
)

SELECT
    Request_Type,
    No_Reopen_SLA_Rate,
    Reopened_SLA_Rate,

    ROUND(
        Reopened_SLA_Rate
        - No_Reopen_SLA_Rate,
        2
    ) AS Reopened_pp

FROM reopen_by_type

ORDER BY Reopened_pp DESC;