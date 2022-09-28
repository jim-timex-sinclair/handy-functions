import pickle
import os

class PickleCache:
    """
    A class mostly set up to avoind having to repeat passing in the cache path.  Create the class once in code, set the cache path
    and then use it again and again to get the pickled function results.
    Pickles a function result and returns it..I found it handy to cache results between tests with long running api calls.
    Test is inline for now.
    """
    def __init__(self) -> None:
        self.__cache_path = ''
    
    @property
    def cache_path(self) -> str:
        return self.__cache_path

    #TODO Add path check
    @cache_path.setter
    def cache_path(self, value : str):
        self.__cache_path = value
        
    def cache_interface(self, function, use_cache : bool, *args):
        """
        The cache_interface is pretty much here just for testing and will not be used in prod...
        """
        global CACHE_PATH
        function_handle = function.__name__
        cache_object = None
        cache_file_name = function_handle + '.p'
        cache_path_file_name = os.path.join(self.__cache_path, cache_file_name)
        if use_cache == True:
            if os.path.exists(cache_path_file_name):
                with open(cache_path_file_name, 'rb') as fin:
                    cache_object = pickle.load(fin)
            else:
                cache_object = function(*args)
                with open(cache_path_file_name, 'wb') as fout:
                    pickle.dump(cache_object, fout)
        else:
            cache_object = function(*args)
            with open(cache_path_file_name, 'wb') as fout:
                pickle.dump(cache_object, fout)
        return cache_object

def local_test1():
    pickle_cache = PickleCache()
    pickle_cache.cache_path = r"C:\Users\james\Source\Repos\handy-functions\data"
    def mytestfunction(x):
        x = x + 1
        return x
    y = pickle_cache.cache_interface(mytestfunction, False, 1)
    print(y)
    #now do it again to make sure the call worked
    y = pickle_cache.cache_interface(mytestfunction, True, 1)
    print(y)

def main():
    """
    Main entry point for test script
    """
    local_test1()
if __name__ == '__main__':
    main()