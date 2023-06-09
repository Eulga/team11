from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

from pymongo import MongoClient

#client = MongoClient('')본인의 db를 연결 하세요
db = client.dbsparta

import uuid

from flask_bcrypt import bcrypt

import tools


# web 구동은 flask사용 DB는 MongoDB 사용

# 메인 페이지
@app.route('/')
def home():
    return render_template('index.html')


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
    try:
        db.team11_guestbook.insert_one(doc)
        result = True
    except:
        result = False

    user = db.team11_guestbook.find_one({'uuid': own_uuid}, {'_id': False, 'password': False})
    print('방명록 등록: ' + str(user))

    return jsonify({'result': result})


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


# 개인 페이지 - 박영준님
@app.route('/yeongjun')
def yeongjun():
    return render_template('yeongjun.html')


# 오늘의 목표 추가 버튼 - 박영준님
@app.route("/yeongjun/bucket", methods=["POST"])
def yeongjun_bucket_post():
    bucket_receive = request.form['bucket_give']
    bucket_list = list(db.yeongjun.find({}, {'_id': False}))
    count = len(bucket_list) + 1

    doc = {
        'num': count,
        'bucket': bucket_receive,
        'done': 0
    }
    db.yeongjun.insert_one(doc)
    return jsonify({'msg': '저장 완료!'})


@app.route("/yeongjun/bucket", methods=["GET"])
def yeongjun_bucket_get():
    all_buckets = list(db.yeongjun.find({}, {'_id': False}))
    return jsonify({'result': all_buckets})


# 완료 버튼 - 박영준님
@app.route("/yeongjun/bucket/done", methods=["POST"])
def yeongjun_bucket_done():
    num_receive = request.form['num_give']
    db.yeongjun.update_one({'num': int(num_receive)}, {'$set': {'done': 1}})
    return jsonify({'msg': '완료!'})


# 취소 버튼 - 박영준님
@app.route("/yeongjun/bucket/reset", methods=["POST"])
def yeongjun_bucket_reset():
    num_receive = request.form['num_give']
    db.yeongjun.update_one({'num': int(num_receive)}, {'$set': {'done': 0}})
    return jsonify({'msg': '취소!'})


# 삭제 버튼 - 박영준님
@app.route("/yeongjun/bucket/delete", methods=["POST"])
def yeongjun_delete_post():
    delete_receive = request.form['delete_give']
    db.yeongjun.delete_one({'num': int(delete_receive)})
    return jsonify({'result': 'success', 'msg': '삭제 완료!'})


# 개인 페이지 - 유시환님
@app.route('/sihwan')
def sihwan():
    return render_template('sihwan.html')


# 오늘의 목표 추가 버튼 - 유시환님
@app.route("/sihwan/bucket", methods=["POST"])
def sihwan_bucket_post():
    bucket_receive = request.form['bucket_give']
    bucket_list = list(db.sihwan.find({}, {'_id': False}))
    count = len(bucket_list) + 1

    doc = {
        'num': count,
        'bucket': bucket_receive,
        'done': 0
    }
    db.sihwan.insert_one(doc)
    return jsonify({'msg': '저장 완료!'})


@app.route("/sihwan/bucket", methods=["GET"])
def sihwan_bucket_get():
    all_buckets = list(db.sihwan.find({}, {'_id': False}))
    return jsonify({'result': all_buckets})


# 완료 버튼 - 유시환님
@app.route("/sihwan/bucket/done", methods=["POST"])
def sihwan_bucket_done():
    num_receive = request.form['num_give']
    db.sihwan.update_one({'num': int(num_receive)}, {'$set': {'done': 1}})
    return jsonify({'msg': '완료!'})


# 취소 버튼 - 유시환님
@app.route("/sihwan/bucket/reset", methods=["POST"])
def sihwan_bucket_reset():
    num_receive = request.form['num_give']
    db.sihwan.update_one({'num': int(num_receive)}, {'$set': {'done': 0}})
    return jsonify({'msg': '취소!'})


# 삭제 버튼 - 유시환님
@app.route("/sihwan/bucket/delete", methods=["POST"])
def sihwan_delete_post():
    delete_receive = request.form['delete_give']
    db.sihwan.delete_one({'num': int(delete_receive)})
    return jsonify({'result': 'success', 'msg': '삭제 완료!'})


# 개인 페이지 - 김광균님
@app.route('/gwanggyun')
def gwanggyun():
    return render_template('gwanggyun.html')


# 오늘의 목표 추가 버튼 - 김광균님
@app.route("/gwanggyun/bucket", methods=["POST"])
def gwanggyun_bucket_post():
    bucket_receive = request.form['bucket_give']
    bucket_list = list(db.gwanggyun.find({}, {'_id': False}))
    count = len(bucket_list) + 1

    doc = {
        'num': count,
        'bucket': bucket_receive,
        'done': 0
    }
    db.gwanggyun.insert_one(doc)
    return jsonify({'msg': '저장 완료!'})


@app.route("/gwanggyun/bucket", methods=["GET"])
def gwanggyun_bucket_get():
    all_buckets = list(db.gwanggyun.find({}, {'_id': False}))
    return jsonify({'result': all_buckets})


# 완료 버튼 - 김광균님
@app.route("/gwanggyun/bucket/done", methods=["POST"])
def gwanggyun_bucket_done():
    num_receive = request.form['num_give']
    db.gwanggyun.update_one({'num': int(num_receive)}, {'$set': {'done': 1}})
    return jsonify({'msg': '완료!'})


# 취소 버튼 - 김광균님
@app.route("/gwanggyun/bucket/reset", methods=["POST"])
def gwanggyun_bucket_reset():
    num_receive = request.form['num_give']
    db.gwanggyun.update_one({'num': int(num_receive)}, {'$set': {'done': 0}})
    return jsonify({'msg': '취소!'})


# 삭제 버튼 - 김광균님
@app.route("/gwanggyun/bucket/delete", methods=["POST"])
def gwanggyun_delete_post():
    delete_receive = request.form['delete_give']
    db.gwanggyun.delete_one({'num': int(delete_receive)})
    return jsonify({'result': 'success', 'msg': '삭제 완료!'})


# 개인 페이지 - 김재익님
@app.route('/jaeik')
def jaeik():
    return render_template('jaeik.html')


# 오늘의 목표 추가 버튼 - 김재익님
@app.route("/jaeik/bucket", methods=["POST"])
def jaeik_bucket_post():
    bucket_receive = request.form['bucket_give']
    bucket_list = list(db.jaeik.find({}, {'_id': False}))
    count = len(bucket_list) + 1

    doc = {
        'num': count,
        'bucket': bucket_receive,
        'done': 0
    }
    db.jaeik.insert_one(doc)
    return jsonify({'msg': '저장 완료!'})


@app.route("/jaeik/bucket", methods=["GET"])
def jaeik_bucket_get():
    all_buckets = list(db.jaeik.find({}, {'_id': False}))
    return jsonify({'result': all_buckets})


# 완료 버튼 - 김재익님
@app.route("/jaeik/bucket/done", methods=["POST"])
def jaeik_bucket_done():
    num_receive = request.form['num_give']
    db.jaeik.update_one({'num': int(num_receive)}, {'$set': {'done': 1}})
    return jsonify({'msg': '완료!'})


# 취소 버튼 - 김재익님
@app.route("/jaeik/bucket/reset", methods=["POST"])
def jaeik_bucket_reset():
    num_receive = request.form['num_give']
    db.jaeik.update_one({'num': int(num_receive)}, {'$set': {'done': 0}})
    return jsonify({'msg': '취소!'})


# 삭제 버튼 - 김재익님
@app.route("/jaeik/bucket/delete", methods=["POST"])
def jaeik_delete_post():
    delete_receive = request.form['delete_give']
    db.jaeik.delete_one({'num': int(delete_receive)})
    return jsonify({'result': 'success', 'msg': '삭제 완료!'})


# 개인 페이지 - 이명현님
@app.route('/myeonghyeon')
def myeonghyeon():
    return render_template('myeonghyeon.html')


# 오늘의 목표 추가 버튼 - 이명현님
@app.route("/myeonghyeon/bucket", methods=["POST"])
def myeonghyeon_bucket_post():
    bucket_receive = request.form['bucket_give']
    bucket_list = list(db.myeonghyeon.find({}, {'_id': False}))
    count = len(bucket_list) + 1

    doc = {
        'num': count,
        'bucket': bucket_receive,
        'done': 0
    }
    db.myeonghyeon.insert_one(doc)
    return jsonify({'msg': '저장 완료!'})


@app.route("/myeonghyeon/bucket", methods=["GET"])
def myeonghyeon_bucket_get():
    all_buckets = list(db.myeonghyeon.find({}, {'_id': False}))
    return jsonify({'result': all_buckets})


# 완료 버튼 - 이명현님
@app.route("/myeonghyeon/bucket/done", methods=["POST"])
def myeonghyeon_bucket_done():
    num_receive = request.form['num_give']
    db.myeonghyeon.update_one({'num': int(num_receive)}, {'$set': {'done': 1}})
    return jsonify({'msg': '완료!'})


# 취소 버튼 - 이명현님
@app.route("/myeonghyeon/bucket/reset", methods=["POST"])
def myeonghyeon_bucket_reset():
    num_receive = request.form['num_give']
    db.myeonghyeon.update_one({'num': int(num_receive)}, {'$set': {'done': 0}})
    return jsonify({'msg': '취소!'})


# 삭제 버튼 - 이명현님
@app.route("/myeonghyeon/bucket/delete", methods=["POST"])
def myeonghyeon_delete_post():
    delete_receive = request.form['delete_give']
    db.myeonghyeon.delete_one({'num': int(delete_receive)})
    return jsonify({'result': 'success', 'msg': '삭제 완료!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)
