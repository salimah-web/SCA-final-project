from application import db, app


def main():
    db.create_all()
    print('DB created successfully.')


if __name__ == '__main__':
    app.app_context().push()
    main()
