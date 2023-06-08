from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

from pymongo import MongoClient

# client = MongoClient('mongodb+srv://Sparta:test@cluster0.90mpqge.mongodb.net/?retryWrites=true&w=majority')
client = MongoClient('mongodb+srv://sparta:test@cluster0.r2nnoby.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

import uuid

from flask_bcrypt import bcrypt

import tools


# web 구동은 flask사용 DB는 MongoDB 사용


@app.route('/')
def home():
    return render_template('indexHome.html')

@app.route('/main')
def gomain():
    return render_template('indexmain.html')


# 자기소개 텍스트 정보 불러오기
@app.route('/introductionData')
def introductionData():
    data = list(db.team11.find({}, {'_id': False}))

    return jsonify({'data': data})


# 로그인


# 방명록 등록
# uuid를 생성해서 끼워 id로 사용한다
# 저장후 다시 불러서 반환해 주는 것으로 신뢰성?을 보장했다
@app.route("/guestbook_save", methods=["POST"])
def guestbook_save():
    name_receive = request.form['name_give']
    pw_receive = request.form['password_give']
    guestbook_receive = request.form['guestbook_give']

    # 비밀번호를 해시코드로 암호화
    pw_hash = bcrypt.hashpw(pw_receive.encode("utf-8"), bcrypt.gensalt())
    own_uuid = str(uuid.uuid4())

    doc = {
        'name': name_receive,
        'guestbook': guestbook_receive,
        'password': pw_hash,
        'uuid': own_uuid
    }
    db.team11_guestbook.insert_one(doc)
    user = db.team11_guestbook.find_one({'uuid': own_uuid}, {'_id': False, 'password': False})

    print(user['name'])

    return jsonify({'user': user})


# 방명록 조회
@app.route("/guestbook_read", methods=["GET"])
def guestbook_read():
    all_guestbooks = list(db.team11_guestbook.find({}, {'_id': False, 'password': False}))

    return jsonify({'users': all_guestbooks})


# 방명록 수정
# uuid를 받아서 검색한다 고유성이 확보 되어서 기타 자질구레한 정보가 필요없다.
@app.route("/guestbook_modify", methods=["POST"])
def guestbook_modify():
    pw_receive = request.form['password_give']
    uuid_receive = request.form['uuid_give']
    new_guestbook_receive = request.form['new_guestbook_give']

    user = db.team11_guestbook.find_one({'uuid': uuid_receive}, {'_id': False})

    result = tools.check_password(pw_receive, user['password'])

    if result:
        db.team11_guestbook.update_one({
            'uuid': uuid_receive,
        },
            {
                '$set': {
                    'guestbook': new_guestbook_receive
                }
            }
        )
        user = db.team11_guestbook.find_one({'uuid': uuid_receive}, {'_id': False, 'password': False})
        return jsonify({'user': user, 'result': result})

    return jsonify({'result': result})


# 방명록 삭제
@app.route("/guestbook_delete", methods=["POST"])
def guestbook_delete():
    pw_receive = request.form['password_give']
    uuid_receive = request.form['uuid_give']

    user = db.team11_guestbook.find_one({'uuid': uuid_receive}, {'_id': False})

    result = tools.check_password(pw_receive, user['password'])
    if result:
        db.team11_guestbook.delete_one({'uuid': uuid_receive, })

    return jsonify({'result': result})


@app.route("/test", methods=["GET"])
def test():
    user = db.team11_guestbook.find_one({'uuid': '362f74ee-ff9e-432f-8998-8aaa4e2c2fbc'}, {'_id': False})

    return jsonify({'user': user})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
