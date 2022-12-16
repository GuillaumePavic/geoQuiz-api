from dbConnect import connection

class Quiz:
    questionsTotal = 3

    @staticmethod
    def getData(category, level):
        sql = """
        SELECT 
        "country"."id",
        "country"."short_name",
        "country"."capital",
        "continent"."label" AS "continent",
        "level"."label" AS "level"
        FROM "country"
        JOIN "continent" ON "continent_id" = "continent"."id"
        JOIN "level" ON "level_id" = "level"."id"
        WHERE "continent"."label" = %s AND "level"."label"  = %s 
        ORDER BY random()
        LIMIT %s;
        """

        with connection:
            with connection.cursor() as cursor:
                cursor.execute(sql, (category, level, Quiz.questionsTotal))
                results = cursor.fetchall()
                
                formattedResults = []
                for result in results:
                    formattedResults.append({
                        "id": result[0],
                        "country": result[1],
                        "capital": result[2],
                        "category": result[3],
                        "level": result[4],
                    })

                return formattedResults