import database as db
import datetime as dt
import core.exceptions as exc
import models
import logging

logger = logging.getLogger('uvicorn.error')


class NumericMetrics():
    
    def __init__(self, user_id):
        self.user_id = user_id
        pass

    async def getSoldProducts(
            self, 
            connection:db.asyncpg.Connection = None,
            startDate:dt.date =  None,
            endDate:dt.date =dt.date.today()
    ) -> float:
        if not connection:
            connection = await db.getConnection()
        if not startDate:
            startDate = endDate - dt.timedelta(days=30)
        logger.debug(f"Get products sold by manager {self.user_id} in ({startDate.isoformat()} - {endDate.isoformat()})")
        try:
            return await connection.fetchval(
                """
                    SELECT SUM(amount)
                    FROM sales 
                    WHERE dt_rep >= $1 and dt_rep <= $2 and manag_id = $3;
                """,
                startDate,
                endDate,
                self.user_id
            )
        except Exception as err:
            logger.critical(err)
            exc.BaseAPIException(message="Something wrong with app!", status_code=500)

    async def getSalesPlan(
            self, 
            connection:db.asyncpg.Connection = None,
            month:int = dt.date.today().month
    ) -> models.SalesPlan:
        if not connection:
            connection = await db.getConnection()
        logger.debug(f"Get sales plan by manager {self.user_id} at month num {month}")
        try:
            todayDate = dt.date.today()
            result = await connection.fetchrow(
                """
                    select 
                        SUM(case when p.category = 'Sales_amount' then p.plan else 0 end) as sales_amount,
                        SUM(case when p.category = 'New_cln' then p.plan else 0 end) as new_clients
                    from "plans" p
                    where 
                        p.dt_rep >= $1 
                        and p.dt_rep < $2
                        and p.manag_id = $3;
                """,
                dt.date(year=todayDate.year, month=month, day=1),
                dt.date(
                    year=todayDate.year if month+1<=12 else todayDate.year+1,
                    month=month if month+1 <= 12 else 1, 
                    day=1
                ),
                self.user_id
            )
            return models.SalesPlan(sales_amount=result['sales_amount'], new_clients=result['new_clients'])
        except Exception as err:
            logger.critical(err)
            exc.BaseAPIException(message="Something wrong with app!", status_code=500)

    async def getUserEfficiency(
            self, 
            connection:db.asyncpg.Connection = None,
            month:int = dt.date.today().month
        ):
        if not connection:
            connection = await db.getConnection()
        logger.debug(f"Get user efficiency by manager {self.user_id} at month num {month}")
        try:
            todayDate = dt.date.today()
            result = await connection.fetchrow(
                """
                """,
                dt.date(year=todayDate.year, month=month, day=1),
                dt.date(
                    year=todayDate.year if month+1<=12 else todayDate.year+1,
                    month=month if month+1 <= 12 else 1, 
                    day=1
                ),
                self.user_id
            )
            return models.SalesPlan(sales_amount=result['sales_amount'], new_clients=result['new_clients'])
        except Exception as err:
            logger.critical(err)
            exc.BaseAPIException(message="Something wrong with app!", status_code=500)
    
    async def getUserNewCustomers(
        self, 
        connection:db.asyncpg.Connection = None,
    ):
        if not connection:
            connection = await db.getConnection()
        logger.debug(f"Get user new customers by manager {self.user_id}")
        try:
            return await connection.fetchval(
                """
                    select coalesce(count(distinct c.id),0) 
                    from customers c
                    where c.manag_id = $1 and c.dt_reg >= now()::date - 30;;
                """,
                self.user_id
            )
        except Exception as err:
            logger.critical(err)
            exc.BaseAPIException(message="Something wrong with app!", status_code=500)