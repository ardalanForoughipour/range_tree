import sys


class Node:
    def __init__(self, range_start, range_end):
        self.start = range_start
        self.end = range_end
        self.parent = None
        self.left = None
        self.right = None
        self.height = 1
        self.contained_ranges = []


class RangeTree:

    def __init__(self):
        self.root = None

    def minimum_node(self, node):
        while node.left is not None:
            node = node.left
        return node

    def getHeight(self, node):
        if not node:
            return 0
        return node.height

    def getBalance(self, node):
        if not node:
            return 0
        return self.getHeight(node.right) - self.getHeight(node.left)

    def leftRotate(self, z):
        y = z.right
        T2 = y.left

        # Perform rotation
        y.left = z
        y.parent = z.parent
        z.parent = y

        z.right = T2
        if T2 is not None:
            T2.parent = z
        # Update heights
        z.height = 1 + max(self.getHeight(z.left),
                           self.getHeight(z.right))
        y.height = 1 + max(self.getHeight(y.left),
                           self.getHeight(y.right))
        # Return the new root
        return y

    def rightRotate(self, z):
        y = z.left
        T3 = y.right
        # Perform rotation
        y.right = z
        y.parent = z.parent
        z.parent = y.parent

        z.left = T3
        if T3 is not None:
            T3.parent = z
        # Update heights
        z.height = 1 + max(self.getHeight(z.left),
                           self.getHeight(z.right))
        y.height = 1 + max(self.getHeight(y.left),
                           self.getHeight(y.right))
        # Return the new root
        return y

    def __search_tree_exact_range_helper(self, node, start, end):
        if node is None or (start == node.start and end == node.end):
            return node

        if end < node.start:
            return self.__search_tree_exact_range_helper(node.left, start, end)
        elif start > node.end:
            return self.__search_tree_exact_range_helper(node.right, start, end)
        else:
            print("TODO")
            return None

    def __inorder(self, node):
        if node is None:
            return
        self.__inorder(node.left)
        v = "(" + str(node.start) + " , " + str(node.end) + "," + str(node.contained_ranges) +")"
        print(v, end=" ")
        self.__inorder(node.right)

    def __preorder(self, node):
        if node is None:
            return

        v = "(" + str(node.start) + " , " + str(node.end) + "," + str(node.contained_ranges) +")"
        print(v, end=" ")
        self.__preorder(node.left)
        self.__preorder(node.right)

    def __postorder(self, node):
        if node is None:
            return
        self.__postorder(node.left)
        self.__postorder(node.right)
        v = "(" + str(node.start) + " , " + str(node.end) + "," + str(node.contained_ranges) +")"
        print(v, end=" ")

    def get_inorder_treversal(self):
        self.__inorder(self.root)
        print()

    def get_postorder_treversal(self):
        self.__postorder(self.root)
        print()

    def get_preorder_treversal(self):
        self.__preorder(self.root)
        print()

    def __deleteNodeHelper(self, node, start, end):
        if node is None:
            return node

        elif end < node.start:
            node.left = self.__deleteNodeHelper(node.left, start, end)
        elif start > node.end:
            node.right = self.__deleteNodeHelper(node.right, start, end)


        # start == node.start and end == node.end
        else:
            # the key has been found, now delete it
            if node.left == None:
                temp = node.right
                node = None
                return temp
            elif node.right == None:
                temp = node.left
                node = None
                return temp
            else:
                temp = self.minimum_node(node.right)
                node.start = temp.start
                node.end = temp.end
                node.right = self.__deleteNodeHelper(node.right, temp.start, temp.end)

        if node is None:
            return node
        node.height = 1 + max(self.getHeight(node.left),
                              self.getHeight(node.right))
        balance = self.getBalance(node)

        # Case 1 - Left Left
        if balance == -2 and self.getBalance(node.left) <= 0:
            return self.rightRotate(node)

        # Case 2 - Right Right
        if balance == 2 and self.getBalance(node.right) >= 0:
            return self.leftRotate(node)

        # Case 3 - Left Right
        if balance == -2 and self.getBalance(node.left) > 0:
            node.left = self.leftRotate(node.left)
            return self.rightRotate(node)

        # Case 4 - Right Left
        if balance == 2 and self.getBalance(node.right) < 0:
            node.right = self.rightRotate(node.right)
            return self.leftRotate(node)

        return node

    def search_tree_for_exact_range(self, start, end):
        return self.__search_tree_exact_range_helper(self.root, start, end)

    def __get_contained_ranges(self, node, start, end):
        l = []
        if node is None:
            return l
        if start <= node.start and end >= node.end:
            t = (node.start, node.end)
            l.append(t)
        l = l + self.__get_contained_ranges(node.left, start, end)
        l = l + self.__get_contained_ranges(node.right, start, end)
        return l

    def __insert(self, start, end, node):

        # lesser range
        if end < node.start:
            if node.left is None:
                nn = Node(start, end)
                node.left = nn
                nn.parent = node

            else:
                node.left = self.__insert(start, end, node.left)

        # greater range
        elif start > node.end:
            if node.right is None:
                nn = Node(start, end)
                node.right = nn
                nn.parent = node
            else:
                node.right = self.__insert(start, end, node.right)

        # contained range
        elif start > node.start and end<node.end:
            node.contained_ranges.append((start, end))
        # containing range
        elif start <= node.start and end >= node.end:
            pass
            l = []
            l = l + self.__get_contained_ranges(node.left, start, end)
            l = l + self.__get_contained_ranges(node.right, start, end)
            for i in l:
                self.__deleteNodeHelper(node, i[0], i[1])
                node.contained_ranges.append((i[0], i[1]))
            node.contained_ranges.append((node.start, node.end))
            node.start = start
            node.end = end

        # intersected range
        else:
            raise ValueError("intersected range")


        node.height = 1 + max(self.getHeight(node.left), self.getHeight(node.right))

        balance = self.getBalance(node)

        if balance == -2:
            # left left
            if end < node.left.start:
                return self.rightRotate(node)
            # left right
            else:
                node.left = self.leftRotate(node.left)
                return self.rightRotate(node)
        elif balance == 2:
            #right right
            if start > node.right.end:
                return self.leftRotate(node)
            # right left
            else:
                node.right = self.rightRotate(node.right)
                return self.leftRotate(node)
        return node

    def insert(self, start, end):
        if end < start:
            raise ValueError("Invalid Range, Start is bigger than end")
        if self.root is None:
            self.root = Node(start, end)
            return
        self.root = self.__insert(start, end, self.root)


    def get_contained_ranges(self,start, end):
        return self.__get_contained_ranges(self.root,start,end)


    # delete the node from the tree
    def deleteNode(self, start, end):
        self.root = self.__deleteNodeHelper(self.root, start, end)

    def __check_is_avl(self, node):
        if node is None:
            return True, 0
        right_res, rh = self.__check_is_avl(node.right)
        left_res, lh = self.__check_is_avl(node.left)
        h = (max(rh, lh) + 1)
        if not right_res:
            return False, h
        if not left_res:
            return False, h
        if rh - lh < -1 or rh - lh > 1:
            return False, h
        return True, h

    def check_is_avl(self):
        return self.__check_is_avl(self.root)


# if __name__ == "__main__":
#     tree = RangeTree()
#     tree.insert(10, 20)
#     tree.insert(30, 49)
#     tree.insert(50, 60)
#     tree.insert(61, 70)
#     tree.insert(50, 70)
#     # print(tree.get_contained_ranges(50,70))
#     # tree.deleteNode(10,20)
#     tree.get_inorder_treversal()
#     tree.get_preorder_treversal()