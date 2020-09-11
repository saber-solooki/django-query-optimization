def query_reporter(func):
    def func_wrapper(*attr, **kwargs):
        from django.db import connection
        from django.db import reset_queries
        import time
        reset_queries()

        start = time.time()

        result = func(*attr, **kwargs)

        end = time.time()

        print(len(connection.queries))
        for q in connection.queries:
            print("\n")
            print(q)
        print("\n")
        print(end - start)

        return result

    return func_wrapper


class QueryReporterMixin:
    def dispatch(self, request, *args, **kwargs):
        from django.db import connection
        from django.db import reset_queries
        import time
        reset_queries()

        start = time.time()

        result = super(QueryReporterMixin, self).dispatch(request, *args, **kwargs)

        end = time.time()

        print(len(connection.queries))
        for q in connection.queries:
            print("\n")
            print(q)
        print("\n")
        print(end - start)

        return result
