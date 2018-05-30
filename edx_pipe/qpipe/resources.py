from __future__ import print_function

import re
import os

import util
from helperclasses import DictionaryTable


class Node(object):
    def __init__(self, uri):
        self._id = None
        self.uri = uri
        self.parent_id = None
        self.child_number = None
        self.children = []

    def append_child(self, node):
        '''
        Sets the parent_id attribute of appended child
        '''
        if node:
            self.children.append(node)
            node.parent_id = self._id

    def __str__(self, increment='-'):
        return self.print_lineage(self, increment, increment)

    def print_lineage(self, node, indent, increment):
        # Print the node's URI at the current indentaion level
        result = indent + ' ' + node.uri + '\n'
        # Recursively print each child with incremented indentation
        for child_node in node.children:
            result += self.print_lineage(child_node, indent + increment,
                                         increment)
        return result


class Resource(Node):
    def __init__(self, uri, resource_name=''):
        super(Resource, self).__init__(uri)
        self.resource_name = resource_name
        self.content = None
        self.medium = None
        self.resource_type_id = None

    def merge(self, node):
        new_resource_name = node.resource_name
        if new_resource_name and not self.resource_name:
            self.resource_name = new_resource_name

    def get_row(self):
        return {
            'resource_id': self._id,
            'resource_name': self.resource_name,
            'resource_uri': self.uri,
            'resource_type_id': self.resource_type_id,
            'resource_parent_id': self.parent_id
        }


class Problem(Node):
    CHILD_NUMBER = re.compile('/(?P<child_number>\d{1,2})/?$')

    def __init__(self, module_uri):
        super(Problem, self).__init__(module_uri)
        self.resource_id = None

    def merge(self, node):
        new_resource_id = node.resource_id
        if new_resource_id and not self.resource_id:
            self.resource_id = new_resource_id

    def get_row(self):
        return {
            'problem_id': self._id,
            'problem_name': self.uri,
            'resource_id': self.resource_id,
            'problem_parent_id': self.parent_id,
            'problem_child_number': self.get_child_number()
        }

    def get_child_number(self):
        match = self.CHILD_NUMBER.search(self.uri)
        if match:
            return match.group('child_number')


class ResourceHierarchy(object):
    def __init__(self, moocdb_table, root='', NodeType=Node):
        self.size = 0

        # Set root node
        root = NodeType(root)
        root.resource_id = 0
        self.hierarchy = root

        # Set MOOCdb table object that
        # the resources are going to be
        # written to.
        self.resources = moocdb_table

    def __str__(self, increment='*'):
        printed_tree = ' Resource Hierarchy : \n' + self.hierarchy.__str__(
            increment)
        return printed_tree

    # Inserts a resource in the hierarchy, with all necessary intermediary nodes.
    # Updates the discovered urls list
    def insert(self, resource_node):
        # First, check if the url is new
        uri = resource_node.uri
        known_parent = self.get_known_parent(uri)
        if known_parent.uri == uri:
            known_parent.merge(resource_node)
            return known_parent._id
        else:
            parent_uri = known_parent.uri
            # Split uri at the point it is new
            new_levels = [parent_uri, uri[len(parent_uri):]]
            # Build the vertical tree to insert
            tree_to_insert = self.prepare_resource_for_insert(resource_node,
                                                              new_levels)
            # Insert the tree at the appropriate location
            known_parent.append_child(tree_to_insert)
            inserted_resource_id = self.size
            return inserted_resource_id

    def affect_identifier_to(self, node):
        self.size += 1
        node._id = self.size

    def get_known_parent(self, uri):
        def rec_search(node, uri):
            search_under = None
            for child in node.children:
                if child.uri in uri:
                    search_under = child
                    break
            if search_under:
                return rec_search(search_under, uri)
            else:
                return node

        return rec_search(self.hierarchy, uri)

    def rec_store_resource(self, node):
        self.resources.store(node.get_row())

        for child in node.children:
            self.rec_store_resource(child)

    def serialize(self, pretty_print_to=''):
        self.rec_store_resource(self.hierarchy)

        if pretty_print_to:
            try:
                hierarchy_file = open(pretty_print_to, 'w')
                hierarchy_file.write(self.__str__())
                hierarchy_file.close()
            except IOError:
                print('Failed to open: %s' % pretty_print_to)

    #------------------------------
    # Auxiliary functions
    # Used to perform insertion
    #------------------------------

    # Create a list of intermediary nodes to insert before the resource
    # Takes ['http://a', 'b/c/d/'] as argument, where:
    # - 'http://a/b/c/d/' is the URI of the resource to insert
    # - 'http://a/' is the known prefix of the resource to insert
    def build_intermediary_nodes(self, new_levels, NodeType):
        if new_levels[1] == '':
            return
        else:
            # Split new levels
            new_levels_list = new_levels[1].split('/')
            # TODO I could just cut-off the list before the last non '' level
            # Instead of the two steps below :
            # 1-Remove possible trailing ''

            while new_levels_list[len(new_levels_list) - 1] == '':
                new_levels_list.pop()
            # 2-Remove last level, corresponding to the original resource node itself
            new_levels_list.pop()

            # Instanciate Resources
            intermediary_uri = new_levels[0]
            intermediary_nodes = []
            for level in new_levels_list:
                intermediary_uri += level + '/'
                new_node = NodeType(intermediary_uri)
                intermediary_nodes.append(new_node)
            return intermediary_nodes

    # Takes a list of URIs ordered from shortest to longest
    # Returns a vertical tree with shortest as ancestor and longest as child
    # Each nodes are given identifiers, and the tree is ready for insertion
    # Note that intermediary nodes have no metadata
    # TODO : Ideally, identifiers should be given once the insertion is completed..
    def prepare_list_for_insert(self, node_list):
        def rec_construct_tree(node_list):
            if not node_list:
                return None
            else:
                next_node = node_list.pop(0)
                self.affect_identifier_to(next_node)
                if len(node_list) > 0:
                    a = rec_construct_tree(node_list)
                    next_node.append_child(a)
                return next_node

        return rec_construct_tree(node_list)

    # Takes a resource node, and returns the corresponding subtree
    # of new resources, ready to insert.
    def prepare_resource_for_insert(self, resource_node, new_levels):
        if new_levels[1] == '':
            return None
        else:
            NodeType = resource_node.__class__
            intermediary_nodes = self.build_intermediary_nodes(new_levels,
                                                               NodeType)
            intermediary_nodes.append(resource_node)
            return self.prepare_list_for_insert(intermediary_nodes)


class ResourceManager(object):
    # Rules for determining content and medium
    def __init__(self, moocdb, HIERARCHY_ROOT='https://'):
        self.resource_hierarchy = ResourceHierarchy(
            moocdb.csv_writers['resources'], HIERARCHY_ROOT, Resource)

        self.resource_types = DictionaryTable(moocdb, 'resource_types')
        self.resources_urls = DictionaryTable(moocdb, 'resources_urls')

        self.content_rules = {
            'video': 'lecture',
            'book': 'book',
            'problem': 'problem',
            'combinedopenended': 'problem',
            'wiki': 'wiki',
            'thread|forum|discussion': 'forum',
            'info': 'informational',
            'preview': 'testing',
            'about': 'informational',
            'progress': 'informational',
            'profile|login|account': 'profile',
            'open_ended': 'problem'
        }

        self.medium_rules = {
            'video': 'video',
            'book': 'text',
            'problem': 'text',
            'combinedopenended': 'text',
            'wiki': 'text',
            'thread|forum|discussion': 'text',
            'info': 'text',
            'about': 'text',
            'progress': 'text',
            'profile': 'text',
            'open_ended': 'text'
        }

    def create_resource(self, event):
        resource_uri = event.get_uri()
        resource_name = event.get_resource_display_name()

        # Sometimes the event comes with no URI
        if not resource_uri:
            return None

        new_resource = Resource(resource_uri, resource_name)
        new_resource_type = self.determine_resource_type(event)

        # Inserts resource into hierarchy
        # Sets the resource's id and type

        new_resource.content = new_resource_type[0]
        new_resource.medium = new_resource_type[1]

        # Record resource url mapping
        new_resource_id = self.resource_hierarchy.insert(new_resource)
        self.resources_urls.insert((new_resource_id, event['url_id']))

        # Return resource ID generated at insertion in the hierarchy
        return new_resource_id

    def determine_resource_type(self, event):
        # Build an array with the useful attributes
        # for making the inference
        array = {}
        array['class_name'] = event.__class__.__name__
        array['uri'] = event.get_uri()
        array['resource_name'] = event['resource_display_name']

        content = None
        for (regex, category) in self.content_rules.iteritems():
            if util.match_regex([regex], "uri", array):
                content = category
                break

        medium = None
        for (regex, category) in self.medium_rules.iteritems():
            if util.match_regex([regex], "uri", array):
                medium = category
                break

        return (content, medium)

    # Functions to build resource type dictionary table
    # and set resource_type_id values.

    def get_resource_types(self):
        """Called at the end of the event processing, when the resource hierarchy is
        completely built. Creates the list of resource types that will be used
        to populate resource_types table"""
        self.rec_set_resource_type_id(self.resource_hierarchy.hierarchy)

    def rec_set_resource_type_id(self, node):
        """Recursively affect resource_type_id to a node and its children"""
        node.resource_type_id = self.resource_types.insert(
            (node.content, node.medium))

        for child in node.children:
            self.rec_set_resource_type_id(child)

    def serialize(self, pretty_print_to=''):
        self.get_resource_types()
        self.resource_hierarchy.serialize(pretty_print_to)
        self.resource_types.serialize()
        self.resources_urls.serialize()
