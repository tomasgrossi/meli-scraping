from ..schemas import Response

def try_except(error_msg):
    
    def interal_deco(func):
        
        def inner(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)

            except Exception as ex:
                print(ex)
                return Response(status_code=500, message=ex)

        
        return inner
    return interal_deco
    
    