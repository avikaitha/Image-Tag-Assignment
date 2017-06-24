import flickrapi
import psycopg2
import traceback
import threading


def data_walker(method, searchstring='*/photo', **params):
    """Calls 'method' with page=0, page=1 etc. until the total
    number of pages has been visited. Yields the photos
    returned.

    Assumes that ``method(page=n, **params).findall(searchstring)``
    results in a list of interesting elements (defaulting to photos),
    and that the toplevel element of the result contains a 'pages'
    attribute with the total number of pages.
    """

    page = 1
    total = 1  # We don't know that yet, update when needed
    while page <= total:
        # Fetch a single page of photos
        # LOG.debug('Calling %s(page=%i of %i, %s)' %
        #           (method.func_name, page, total, params))
        rsp = method(page=page, **params)

        photoset = rsp.getchildren()[0]
        total = int(photoset.get('pages'))

        photos = rsp.findall(searchstring)

        # Yield each photo
        for photo in photos:
            yield photo

        # Ready to get the next page
        page += 1

def keywithmaxval(d):
    """ a) create a list of the dict's keys and values;
        b) return the key with the max value"""
    v = list(d.values())
    k = list(d.keys())
    return k[v.index(max(v))]


def addslashes(s):
    d = {'"':'\\"', "'":"''", "\0":"\\\0", "\\":"\\\\"}
    return ''.join(d.get(c, c) for c in s)



def get_users(api_key,api_secret,initial_user,log=0):
    try:
        conn = psycopg2.connect("dbname='flickr2' user='postgres' host='129.219.60.22' password='password'")
        print "Successfully connected...."
    except:
        pass
    cur = conn.cursor()
    crawl_queue = {}
    flickr = flickrapi.FlickrAPI(api_key, api_secret,format='etree')

    contacts = data_walker(flickr.contacts.getPublicList, searchstring='*/contact',
                                    per_page=1000, user_id= initial_user) #'11378508@N08'
    user_id = initial_user
    print "Initial user: ",user_id
    for contact in contacts:
        crawl_queue[contact.attrib['nsid']] = 1
        # print "Initial: ",initial_user,": ",crawl_queue
        st = "Insert into users(id,username) values ('" + contact.attrib['nsid'] + "','" + addslashes(
            contact.attrib['username']) + "')"
        try:
            cur.execute(st)
            conn.commit()
        except:
            if log == 1: traceback.print_exc()
            conn.rollback()

        st2 = "Insert into fellowship(user_id,follow_id) values ('" + user_id + "','" + contact.attrib['nsid'] + "')"
        try:
            cur.execute(st2)
            conn.commit()
        except:
            if log == 1: traceback.print_exc()
            conn.rollback()


    crawled = [initial_user]
    # print "Initial User: ",initial_user," Crawl Queue",crawl_queue
    # print initial_user,crawled
    while True:
        if len(crawled) >= 300 or len(crawled) == 0:
            break
        if len(crawl_queue) != 0:
            print "Seed: ",initial_user,"Current heap size: ", len(crawl_queue)
            print "Seed: ",initial_user,"Users crawled: ",len(crawled)
            user_id_key = keywithmaxval(crawl_queue)
            del crawl_queue[keywithmaxval(crawl_queue)]
        # print "Popped: ",user_name

            crawled += [user_id_key]
            try:
                contacts = data_walker(flickr.contacts.getPublicList, searchstring='*/contact',
                                        per_page=1000, user_id= user_id_key)
                for contact in contacts:
                    if contact.attrib['nsid'] not in crawled:
                        if contact.attrib['nsid'] not in crawl_queue:
                            crawl_queue[contact.attrib['nsid']] = 1
                        else:
                            crawl_queue[contact.attrib['nsid']] += 1

                    st = "Insert into users(id,username) values ('" + contact.attrib['nsid'] + "','" + addslashes(
                        contact.attrib['username']) + "')"
                    try:
                        cur.execute(st)
                        conn.commit()
                    except:
                        if log == 1: traceback.print_exc()
                        conn.rollback()

                    st2 = "Insert into fellowship(user_id,follow_id) values ('" + user_id_key + "','" + contact.attrib['nsid'] + "')"
                    try:
                        cur.execute(st2)
                        conn.commit()
                    except:
                        if log == 1: traceback.print_exc()
                        conn.rollback()
            except:
                if log == 1: traceback.print_exc()
                print "No contacts!"
    conn.close()




def main():
    count = 0
    """
    Denis	        49503178703@N01	        https://www.flickr.com/photos/mandokid1        birds
    Michael Sauer	107477241@N02	        https://www.flickr.com/photos/107477241@N02        flower
    Jojo	        27295726@N07	        https://www.flickr.com/photos/27295726@N07     nature
    Charlie	        92622665@N08	        https://www.flickr.com/photos/92622665@N08      cars
    a.rios	        39556143@N04	        https://www.flickr.com/photos/rios-enriquez/     foods
    brian	        11677049@N03	        https://www.flickr.com/photos/booksin/page36    abstract
    Jeff Sullivan	58835292@N08	        https://www.flickr.com/photos/jeffreysullivan/page52   nature(mixed)
    Ray Jennings	48790596@N05	        https://www.flickr.com/photos/ray_jennings/    field
    Ale	            21139294@N03	        https://www.flickr.com/photos/aleidarhode/   fashion
    Kramer	        7218844@N03	            https://www.flickr.com/photos/7218844@N03/    art

    """

    seeds = ['49503178703@N01','107477241@N02','27295726@N07','92622665@N08','39556143@N04','11677049@N03','58835292@N08','48790596@N05','21139294@N03','7218844@N03']
    inital_seed_dict = {'49503178703@N01': "Denis",
                        '107477241@N02': "Michael Sauer",
                        '27295726@N07': "Jojo",
                        '92622665@N08': "Charlie",
                        '39556143@N04': "a.rios",
                        '11677049@N03': "brian",
                        '58835292@N08': "Jeff Sullivan",
                        '48790596@N05': "Ray Jennings",
                        '21139294@N03': "Ale",
                        '7218844@N03': "Kramer"
                        }

    api_keys = [u'50447f832b7d99785ebb9ba9b69e6a65',u'82764a924643a98e49381f5f28a9a5a7',u'36eadd83335122d888da119424854efc',u'51da9f4ccbd1dae169eb1e619690530e',u'5ebfd342ebab8ea6b16fbbfe6daf632e']
    api_secrets = [u'11d5ef95815b96b0',u'39c68f2dd019d2c0',u'2bbc80b7476185c5',u'5c473c8f547f07d6',u'1e9c1b2440923add']


    try:
        conn = psycopg2.connect("dbname='flickr2' user='postgres' host='129.219.60.22' password='password'")
        print "Successfully connected...."
    except:
        pass

    cur = conn.cursor()

    for seed in seeds:
        st = "Insert into users(id,username) values ('"+seed+"','"+addslashes(inital_seed_dict[seed])+"')"
        try:
            cur.execute(st)
            conn.commit()
        except:
            traceback.print_exc()
            conn.rollback()


    while count < len(seeds):
        if threading.active_count() <= len(seeds):
            print count
            print "Number of threads: ",threading.active_count()

            t = threading.Thread(target=get_users,args=(api_keys[count%5],api_secrets[count%5],seeds[count]))
            t.start()
            count += 1
if __name__ == '__main__':
    main()