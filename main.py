from connect import db
import argparse
import pymongo


def read_all():
    """
        Retrieve and print all documents from the 'cat' collection.

        This function fetches all cats stored in the collection and prints them.
        If the collection is empty, it notifies the user.

        Raises:
            pymongo.errors.PyMongoError: If a MongoDB-related error occurs.
    """
    try:
        result = db.cat.find({})
        if result.count() == 0:  # Check if the collection is empty
            print("No cats found.")
            return
        for cat in result:
            print(cat)
    except pymongo.errors.PyMongoError as e:
        print(f"Error while reading all cats: {e}")

def read_one():
    """
        Retrieve and print a single document based on the cat's name.

        The user is prompted to input a cat name, which is used to fetch
        and display the matching document. If no match is found, it notifies the user.

        Raises:
            pymongo.errors.PyMongoError: If a MongoDB-related error occurs.
            Exception: For unforeseen errors (e.g., input processing issues).
    """
    try:
        while True:
            user_input = input("Please enter cat name: ")
            cat_name = user_input.split(':')[0]
            result = db.cat.find_one({"name": cat_name})
            if result is None:
                print("Cat not found")
                break
            print(result)
    except pymongo.errors.PyMongoError as e:
        print(f"Error while reading a cat: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def update_age():
    """
        Update the age of a specific cat in the 'cat' collection.

        The user is prompted to input the cat's name and new age.
        The function updates the cat's document with the new age and displays the updated document.

        Raises:
            ValueError: If the user provides an invalid age input (non-numeric).
            pymongo.errors.PyMongoError: If a MongoDB-related error occurs.
            Exception: For unforeseen errors.
    """
    try:
        while True:
            user_input_name = input("Please enter cat name: ")
            user_input_age = input("Please enter cat age: ")
            cat_name = user_input_name.split(':')[0]
            cat_age = int(user_input_age.split(':')[0])
            db.cat.update_one({"name": cat_name}, {"$set": {"age": cat_age}})
            result = db.cat.find_one({"name": cat_name})
            if result is None:
                print("Cat not found")
                break
            print(result)
            break
    except ValueError as e:
        print(f"Invalid input for age: {e}")
    except pymongo.errors.PyMongoError as e:
        print(f"Error while updating cat age: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def update_features():
    """
        Add or update a feature for a specific cat in the 'cat' collection.

        The user is prompted to input the cat's name and the new feature.
        The feature is added to the 'features' array of the matching document.

        Raises:
            pymongo.errors.PyMongoError: If a MongoDB-related error occurs.
            Exception: For unforeseen errors.
    """
    try:
        while True:
            user_input_name = input("Please enter cat name: ")
            user_input_feature = input("Please enter cat new feature: ")
            cat_name = user_input_name.split(':')[0]
            cat_feature = user_input_feature.split(':')[0]
            db.cat.update_one({"name": cat_name}, {"$addToSet": {"features": cat_feature}})
            result = db.cat.find_one({"name": cat_name})
            if result is None:
                print("Cat not found")
                break
            print(result)
            break
    except pymongo.errors.PyMongoError as e:
        print(f"Error while updating cat features: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def delete_cat():
    """
        Delete a specific cat's document from the 'cat' collection.

        The user is prompted to input the cat's name, which is used to locate and delete
        the matching document. If no match is found, it notifies the user.

        Raises:
            pymongo.errors.PyMongoError: If a MongoDB-related error occurs.
            Exception: For unforeseen errors.
    """
    try:
        while True:
            user_input_name = input("Please enter cat name: ")
            cat_name = user_input_name.split(':')[0]
            result = db.cat.find_one({"name": cat_name})
            if result is None:
                print("Cat not found")
                break
            db.cat.delete_one({"name": cat_name})
            print("Cat deleted")
            break
    except pymongo.errors.PyMongoError as e:
        print(f"Error while deleting a cat: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def delete_all():
    """
        Delete all documents from the 'cat' collection.

        This function removes all cats from the collection and logs the number of deleted documents.

        Raises:
            pymongo.errors.PyMongoError: If a MongoDB-related error occurs.
            Exception: For unforeseen errors.
    """
    try:
        result = db.cat.delete_many({})
        print(f"Documents deleted: {result.deleted_count}")
    except pymongo.errors.PyMongoError as e:
        print(f"Error while deleting all cats: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    """
        Entry point for the script.

        This block sets up an argument parser to handle user input from the command line.
        Based on the specified action, the corresponding function is called.

        Raises:
            pymongo.errors.PyMongoError: If a MongoDB-related error occurs during connection.
            Exception: For unforeseen errors during script execution.
    """
    try:
        parser = argparse.ArgumentParser(description="Script to interact with MongoDB Cat collection.")
        parser.add_argument(
            "action", choices=["read_all", "read_one", "update_age", "update_features", "delete_one", "delete_all"],
            help="Specify the function to execute: read_all, read_one, update_age, update_features, delete_one, delete_all"
        )
        args = parser.parse_args()

        if args.action == "read_all":
            read_all()
        elif args.action == "read_one":
            read_one()
        elif args.action == "update_age":
            update_age()
        elif args.action == "update_features":
            update_features()
        elif args.action == "delete_one":
            delete_cat()
        elif args.action == "delete_all":
            delete_all()
    except pymongo.errors.PyMongoError as e:
        print(f"Error connecting to MongoDB: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
