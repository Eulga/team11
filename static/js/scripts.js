/*!
* Start Bootstrap - Agency v7.0.12 (https://startbootstrap.com/theme/agency)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-agency/blob/master/LICENSE)
*/
//
// Scripts
// 

window.addEventListener('DOMContentLoaded', event => {

    // Navbar shrink function
    var navbarShrink = function () {
        const navbarCollapsible = document.body.querySelector('#mainNav');
        if (!navbarCollapsible) {
            return;
        }
        if (window.scrollY === 0) {
            navbarCollapsible.classList.remove('navbar-shrink')
        } else {
            navbarCollapsible.classList.add('navbar-shrink')
        }

    };

    // Shrink the navbar 
    navbarShrink();

    // Shrink the navbar when page is scrolled
    document.addEventListener('scroll', navbarShrink);

    //  Activate Bootstrap scrollspy on the main nav element
    const mainNav = document.body.querySelector('#mainNav');
    if (mainNav) {
        new bootstrap.ScrollSpy(document.body, {
            target: '#mainNav',
            rootMargin: '0px 0px -40%',
        });
    }
    ;

    // Collapse responsive navbar when toggler is visible
    const navbarToggler = document.body.querySelector('.navbar-toggler');
    const responsiveNavItems = [].slice.call(
        document.querySelectorAll('#navbarResponsive .nav-link')
    );
    responsiveNavItems.map(function (responsiveNavItem) {
        responsiveNavItem.addEventListener('click', () => {
            if (window.getComputedStyle(navbarToggler).display !== 'none') {
                navbarToggler.click();
            }
        });
    });

});

$(document).ready(function () {
    show_guestbook();
});

// 방명록 조회 후 화면 출력
function show_guestbook() {
    $('#comment-list').empty()
    let count = 0
    setInterval(() => {
        fetch("/guestbook_read")
            .then((res) => res.json())
            .then((response) => {
                let rows = response['users']
                console.log(rows.length, count)
                if (rows.length > count) {
                    for (let i = count; i < rows.length; i++) {
                        let a = rows[i]
                        let name = a['name']
                        let guestbook = a['guestbook']
                        let own_uuid = a['uuid']

                        let temp_html = guestbook_shape(name, own_uuid, guestbook)
                        $('#comment-list').prepend(temp_html)
                    }
                    count = rows.length
                }
            })
    }, 1000)
}

// 방명록 생성
function save_guestbook() {
    let name = $('#name').val()
    let pw = $('#pw').val()
    let guestbook = $('#guestbook').val()

    let formData = new FormData();
    formData.append("name_give", name)
    formData.append("password_give", pw)
    formData.append("guestbook_give", guestbook)

    fetch("/guestbook_save", {method: "POST", body: formData,})
        .then((res) => res.json())
        .then((response) => {
            $('#guestbook').val('')

            let result = response['result']
            if (result) {
                console.log("저장 성공")
            } else {
                console.warn("저장 실패")
            }
        });

}

// 방명록 show, save 시 필요한 방명록 모양
function guestbook_shape(name, own_uuid, guestbook) {
    return `<div id="${own_uuid}">
        <p class="small-name">${name}</p>
        <p class="small-text">${guestbook}</p>
        <div id="edit-guestbook-${own_uuid}" style="display: none">
          <input id="edit-guestbook-text-${own_uuid}" type="text" />
          <input id="edit-guestbook-password-${own_uuid}" type="password" placeholder="비밀번호" />
          <button onclick="modify_guestbook('${own_uuid}')" type="button" class="btn btn-primary">저장</button>
          <button onclick="cancel_edit('${own_uuid}')" type="button" class="btn btn-primary">취소</button>
        </div>
        <button onclick="edit_guestbook('${own_uuid}', '${guestbook}')" type="button"
          class="btn btn-primary">수정</button>
        <button onclick="check_delete_guestbook('${own_uuid}')" type="button" class="btn btn-primary">삭제</button>
        <div id="delete-guestbook-${own_uuid}" style="display: none">
          <input id="delete-guestbook-password-${own_uuid}" type="password" placeholder="비밀번호" />
          <button onclick="delete_guestbook('${own_uuid}')" type="button" class="btn btn-primary">확인</button>
          <button onclick="cancel_delete('${own_uuid}')" type="button" class="btn btn-primary">취소</button>
        </div>
      </div>`
}

// 방명록 수정
function modify_guestbook(own_uuid) {
    let new_guestbook = $(`#edit-guestbook-text-${own_uuid}`).val()
    let pw = $(`#edit-guestbook-password-${own_uuid}`)

    let formData = new FormData();
    formData.append("password_give", pw.val())
    formData.append("new_guestbook_give", new_guestbook)
    formData.append("uuid_give", own_uuid)

    fetch("/guestbook_modify", {method: "POST", body: formData,})
        .then((res) => res.json())
        .then((response) => {
            let result = response['result']

            if (result) {
                let row = response['user']
                $(`#edit-guestbook-${own_uuid}`).hide();
                $(`#${own_uuid} > p.small-text`).text(row['guestbook']).show();
                pw.css({'border': '1px solid black'})
            } else {
                pw.css({'border': '1px solid red'})
                console.log("비밀번호 다름")
            }
        });
}

// 수정 버튼 누를시 작동
function edit_guestbook(own_uuid) {
    let guestbook = $(`#${own_uuid} > p.small-text`)

    guestbook.hide()
    $(`#edit-guestbook-${own_uuid}`).show();
    $(`#edit-guestbook-text-${own_uuid}`).val(guestbook.text());
}

// 수정 버튼 후 취소 버튼 누를 시 작동
function cancel_edit(own_uuid) {
    $(`#edit-guestbook-${own_uuid}`).hide();
    $(`#${own_uuid} > p.small-text`).show();
}

// 방명록 삭제
function delete_guestbook(own_uuid) {
    let pw = $(`#delete-guestbook-password-${own_uuid}`)

    let formData = new FormData();
    formData.append("uuid_give", own_uuid)
    formData.append("password_give", pw.val())

    fetch("/guestbook_delete", {method: "POST", body: formData,})
        .then(res => res.json())
        .then((response) => {
            if (response['result']) {
                $(`#${own_uuid}`).remove()
            } else {
                pw.css({'border': '1px solid red'})
                console.log("비밀번호 다름")
            }
        });
}

// 삭제 버튼 누를시 작동
function check_delete_guestbook(own_uuid) {
    $(`#delete-guestbook-${own_uuid}`).show();
}

function cancel_delete(own_uuid) {
    $(`#delete-guestbook-${own_uuid}`).hide();
}

function modal1(col1) {
    var modalOverlay = document.getElementById('col1-overlay');
    modalOverlay.style.display = 'block';
}

function modal2(col2) {
    var modalOverlay = document.getElementById('col2-overlay');
    modalOverlay.style.display = 'block';
}

function modal3(col3) {
    var modalOverlay = document.getElementById('col3-overlay');
    modalOverlay.style.display = 'block';
}

function modal4(col4) {
    var modalOverlay = document.getElementById('col4-overlay');
    modalOverlay.style.display = 'block';
}

function modal5(col5) {
    var modalOverlay = document.getElementById('col5-overlay');
    modalOverlay.style.display = 'block';
}

function closeIntro1() {
    var modalOverlay = document.getElementById('col1-overlay');
    modalOverlay.style.display = 'none';
}

function closeIntro2() {
    var modalOverlay = document.getElementById('col2-overlay');
    modalOverlay.style.display = 'none';
}

function closeIntro3() {
    var modalOverlay = document.getElementById('col3-overlay');
    modalOverlay.style.display = 'none';
}

function closeIntro4() {
    var modalOverlay = document.getElementById('col4-overlay');
    modalOverlay.style.display = 'none'
}

function closeIntro5() {
    var modalOverlay = document.getElementById('col5-overlay');
    modalOverlay.style.display = 'none';
}