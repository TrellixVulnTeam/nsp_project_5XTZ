import numpy as np
import pandas as pd
import networkx as nx
import sys


class FriendGraph(object):
    """Initialize a FriendGraph object to make friend recommendations"""
    def __init__(self,):
        self.filename = 'followers_data.csv'

    # Put csv data into pandas DataFrame
        self.df = self.load_data(self.filename)
        self.df.drop(['Unnamed: 0'],axis =1,inplace = True)


    # Create networkx graph from DataFrame
        self.G = self.make_network(self.df)


    def load_data(self, filename):
        """Put data into df if file exists"""

        try:
            df = pd.read_csv(filename)
        except IOError:
            raise IOError('Check that file name and path are correct')

        return df




    def make_network(self, df):
        """Take a DataFrame of undirected friendships and return networkx graph object"""

        G = nx.from_pandas_edgelist(df, df.columns[0], df.columns[1])
        return G

    def friends_set(self, G, node):
        """Returns a set of a given user's friends"""
        print(set(G.neighbors(node)))
        return set(G.neighbors(node))

    def friends_of_friends_set(self, G, friends):
        """Given a set of friends, returns a set of friends of friends"""
        friends_of_friends = set()

        for f in friends:
            friends_of_friends.update(G.neighbors(f))
        #print(friends_of_friends)

        return friends_of_friends

    def make_remove_set(self, G, node, friends_of_friends):
        """Removes friends of friends that a user is already friends with"""
        remove_set = set()

        for fof in friends_of_friends:
            if G.has_edge(node, fof):
                remove_set.add(fof)

        return remove_set


    def find_friends_of_friends(self, G, node):
        """Given a user_id, find friends of friends the user is not friends with"""

        # find current friends of user
        friends = self.friends_set(G, node)

        # find friends of friends
        friends_of_friends = self.friends_of_friends_set(G, friends)

        # remove friend_of_friend if fof is friends with user
        remove_set = self.make_remove_set(G, node, friends_of_friends)

        # Remove friends of friends that are in remove set
        friends_of_friends.difference_update(remove_set)

        return list(friends_of_friends)


    def highest_degree(self, G, fof):
        """Given list of friends of friends, return 5 with highest degree"""

        degree_dict = {}
        # Calculate degree for each node, store result in dict
        for f in fof:
            deg = G.degree(f)
            degree_dict[f] = deg

        # Sort by dict values
        sorted_list = sorted(degree_dict, key=degree_dict.get, reverse=True)

        return sorted_list[:5]
    def format_friend_recs(self, user_id, recs):
        """Print 5 friend recommendations to terminal"""

        print ('Friend recommendations for user {0}: {1}'.format(user_id,
                ', '.join(['#'+str(i+1)+': '+str(r) for i, r in enumerate(recs)])))

        lis = [r for i, r in enumerate(recs)]


        return lis


    def recommend_friend(self, user_id):
        """Given a user_id, make 5 friend recommendations"""

        # Find friends of friends of user
        friends_of_friends = self.find_friends_of_friends(self.G, user_id)

        # Find 5 most connected friends of friends
        recommendations = self.highest_degree(self.G, friends_of_friends)


        return self.format_friend_recs(user_id, recommendations)

f = FriendGraph()

list_of_rec = f.recommend_friend(1)
