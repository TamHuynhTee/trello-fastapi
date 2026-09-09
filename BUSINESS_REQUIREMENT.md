# Trello Clone — Business Requirements

## 1. User

- Mỗi User có một tài khoản riêng.
- Mỗi User có thể tham gia nhiều Workspace.
- Mỗi User có thể tham gia nhiều Board.
- Mỗi User có thể được assign vào nhiều Task/Card.
- Một User có thể tạo nhiều Workspace.
- Một User có thể tạo nhiều Board.
- Một User có thể tạo nhiều Task/Card.
- User có thể cập nhật thông tin cá nhân của mình.
- User có thể rời khỏi Workspace nếu không phải Owner duy nhất của Workspace.

---

## 2. Workspace

- Mỗi Workspace phải có ít nhất một Owner.
- Một Workspace có thể có nhiều User.
- Một User có thể tham gia nhiều Workspace.
- User trong Workspace có thể có các role khác nhau:
  - Owner
  - Admin
  - Member

- Owner có quyền quản lý toàn bộ Workspace.
- Admin có thể quản lý member và Board trong Workspace.
- Member chỉ được thao tác trên các Board mà mình có quyền truy cập.
- Một Workspace có thể có nhiều Board.
- Mỗi Board chỉ thuộc một Workspace.
- User có thể được mời vào Workspace.
- User có thể bị remove khỏi Workspace.
- Khi User bị remove khỏi Workspace, quyền truy cập vào các Board thuộc Workspace đó cũng phải được kiểm tra lại.

---

## 3. Board

- Một Workspace có thể có nhiều Board.
- Mỗi Board chỉ thuộc một Workspace.
- Một Board có thể có nhiều User.
- Một User có thể tham gia nhiều Board.
- User trong Board có thể có role:
  - Admin
  - Member
  - Viewer

- Board Admin có thể:
  - cập nhật Board
  - quản lý member
  - tạo List
  - archive Board

- Member có thể tạo và cập nhật Task/Card nếu được cấp quyền.
- Viewer chỉ có quyền xem.
- Một Board có thể có nhiều List.
- Một Board có thể có nhiều Label.
- Board có thể có trạng thái:
  - Active
  - Archived

- Board đã Archived không cho phép tạo mới hoặc chỉnh sửa Task/Card.

---

## 4. List

- Một Board có thể có nhiều List.
- Mỗi List chỉ thuộc một Board.
- List được dùng để đại diện cho một nhóm hoặc trạng thái công việc.

Ví dụ:

- Backlog
- Todo
- In Progress
- Review
- Done

- User có thể tạo List mới.
- User có thể đổi tên List.
- User có thể thay đổi thứ tự các List trong Board.
- User có thể archive List.
- Một List có thể chứa nhiều Task/Card.
- Một Task/Card tại một thời điểm chỉ nằm trong một List.
- Task/Card có thể được di chuyển từ List này sang List khác trong cùng Board.

---

## 5. Task / Card

- Một List có thể có nhiều Task/Card.
- Mỗi Task/Card chỉ thuộc một List tại một thời điểm.
- Mỗi Task/Card phải thuộc một Board thông qua List.
- Một Task/Card có thể được tạo bởi một User.
- Một Task/Card có thể được assign cho nhiều User.
- Một User có thể được assign vào nhiều Task/Card.
- Một Task/Card có thể có:
  - title
  - description
  - members
  - labels
  - due date
  - start date
  - checklist
  - comments
  - attachments

- Title của Task/Card là bắt buộc.
- Description là optional.
- Task/Card có thể được di chuyển giữa các List trong cùng Board.
- Task/Card có thể thay đổi thứ tự trong cùng một List.
- Task/Card có thể được archive.
- Task/Card đã archive không xuất hiện trong danh sách công việc mặc định.

---

## 6. Task Status

Trạng thái của Task/Card có thể được xác định thông qua List.

Ví dụ:

Todo
↓
In Progress
↓
Review
↓
Done

Trong phiên bản đơn giản, có thể quy định các trạng thái cố định:

- TODO
- IN_PROGRESS
- REVIEW
- DONE

Business rules:

- Một Task tại một thời điểm chỉ có một trạng thái.
- User có quyền có thể thay đổi trạng thái Task.
- Khi Task chuyển sang `DONE`, hệ thống có thể lưu thời điểm hoàn thành.
- Task đã hoàn thành vẫn có thể được chuyển lại trạng thái trước đó.
- Không bắt buộc Task phải đi theo thứ tự trạng thái.

Ví dụ hợp lệ:

TODO → DONE

hoặc:

DONE → IN_PROGRESS

---

## 7. Task Priority

Mỗi Task có thể có một mức độ ưu tiên.

Priority gồm:

- LOW
- MEDIUM
- HIGH
- URGENT

Business rules:

- Một Task tại một thời điểm chỉ có một Priority.
- Priority có thể được thay đổi.
- Priority là optional.
- User có thể filter Task theo Priority.

---

## 8. Task Assignment

- Một Task có thể được assign cho nhiều User.
- Một User có thể được assign nhiều Task.
- User chỉ có thể được assign Task nếu User đó là member của Board.
- Không được assign cùng một User nhiều lần vào cùng một Task.
- User có thể tự remove mình khỏi Task nếu có quyền.
- Board Admin có thể add hoặc remove member khỏi Task.

---

## 9. Label

- Một Board có thể có nhiều Label.
- Mỗi Label chỉ thuộc một Board.
- Một Task có thể có nhiều Label.
- Một Label có thể được sử dụng cho nhiều Task.

Ví dụ:

- Bug
- Feature
- Backend
- Frontend
- Urgent

Business rules:

- Không thể sử dụng Label của Board A cho Task thuộc Board B.
- User có thể thêm Label vào Task.
- User có thể remove Label khỏi Task.
- Không được add cùng một Label nhiều lần vào một Task.
- Label có thể có:
  - name
  - color

---

## 10. Due Date

- Một Task có thể có Due Date.
- Due Date là optional.
- User có thể thay đổi Due Date.
- User có thể remove Due Date.
- Hệ thống có thể xác định Task:
  - chưa tới hạn
  - sắp tới hạn
  - quá hạn
  - hoàn thành

- Task quá Due Date nhưng chưa Done được xem là Overdue.
- Task Done không được xem là Overdue.

---

## 11. Comment

- Một Task có thể có nhiều Comment.
- Mỗi Comment chỉ thuộc một Task.
- Mỗi Comment phải được tạo bởi một User.
- User phải có quyền truy cập Board mới được comment.
- User có thể chỉnh sửa Comment của chính mình.
- User có thể xóa Comment của chính mình.
- Board Admin có thể xóa Comment nếu cần.
- Comment phải có nội dung.
- Comment rỗng không được phép tạo.

---

## 12. Checklist

- Một Task có thể có nhiều Checklist.
- Một Checklist chỉ thuộc một Task.
- Một Checklist có thể có nhiều Checklist Item.

Ví dụ:

Task: Implement Login

Checklist:

- Create API
- Validate request
- Hash password
- Write unit test
- Update documentation

Business rules:

- Checklist Item có hai trạng thái:
  - Completed
  - Uncompleted

- User có thể mark Checklist Item là completed.
- User có thể chuyển lại thành uncompleted.
- User có thể thêm, sửa, xóa Checklist Item.
- User có thể thay đổi thứ tự Checklist Item.
- Hệ thống có thể tính tiến độ Checklist.

Ví dụ:

3 / 5 completed

60%

---

## 13. Attachment

- Một Task có thể có nhiều Attachment.
- Một Attachment chỉ thuộc một Task.
- User có quyền truy cập Task có thể upload Attachment.
- Attachment có thể là:
  - image
  - document
  - URL
  - other file

- User có thể xóa Attachment mà mình upload nếu có quyền.
- Hệ thống phải lưu thông tin người upload và thời gian upload.

---

## 14. Drag & Drop

User có thể drag & drop:

- List trong Board.
- Task trong cùng List.
- Task từ List này sang List khác.

Business rules:

- Thứ tự List phải được lưu lại.
- Thứ tự Task trong List phải được lưu lại.
- Sau khi reload trang, thứ tự phải giống với lần sắp xếp gần nhất.
- Khi Task được move sang List khác, Task phải giữ đúng vị trí mới.

---

## 15. Activity History

Hệ thống phải ghi nhận các hoạt động quan trọng.

Ví dụ:

- User created Task.
- User updated Task.
- User moved Task.
- User assigned Member.
- User removed Member.
- User added Label.
- User changed Due Date.
- User added Comment.
- User completed Checklist Item.
- User archived Task.

Business rules:

- Một Board có thể có nhiều Activity.
- Một Task có thể có nhiều Activity.
- Mỗi Activity phải lưu:
  - ai thực hiện
  - hành động gì
  - đối tượng nào
  - thời gian nào

Ví dụ:

John moved "Implement Login API"
from Todo to In Progress.

---

## 16. Search

User có thể search Task theo:

- title
- description

Search chỉ trả về những Task thuộc Board mà User có quyền truy cập.

---

## 17. Filter

User có thể filter Task theo:

- member
- label
- status
- priority
- due date

Ví dụ:

Hiển thị:

- Task HIGH priority
- đang IN_PROGRESS
- assign cho John

Các filter có thể được kết hợp với nhau.

---

## 18. Archive

Các entity sau có thể được Archive:

- Board
- List
- Task

Business rules:

- Archive không đồng nghĩa với delete dữ liệu.
- Dữ liệu archive vẫn tồn tại trong hệ thống.
- Dữ liệu archive mặc định không hiển thị.
- User có quyền có thể xem danh sách archived items.
- User có thể restore archived item.

---

## 19. Permission

Các thao tác phải được kiểm tra quyền ở backend.

Không được chỉ kiểm tra quyền ở frontend.

Ví dụ:

User A không thuộc Board X.

User A gọi:

DELETE /boards/X/tasks/100

Backend phải trả về:

403 Forbidden

hoặc không expose resource và trả:

404 Not Found

tùy theo thiết kế security của hệ thống.

---

## 20. Member Permission

Ví dụ phân quyền:

### Board Admin

Có thể:

- update Board
- archive Board
- add/remove Member
- create/update/archive List
- create/update/archive Task
- assign Member
- manage Label
- delete Comment

### Member

Có thể:

- xem Board
- tạo Task
- update Task
- move Task
- comment
- update Checklist
- assign Task nếu được phép

### Viewer

Chỉ có thể:

- xem Board
- xem List
- xem Task
- xem Comment

Không được chỉnh sửa dữ liệu.

---

# 21. Các Relationship chính cần support

### User — Workspace

Many-to-Many

Một User có thể tham gia nhiều Workspace.

Một Workspace có thể có nhiều User.

---

### Workspace — Board

One-to-Many

Một Workspace có nhiều Board.

Một Board chỉ thuộc một Workspace.

---

### User — Board

Many-to-Many

Một User có thể tham gia nhiều Board.

Một Board có thể có nhiều User.

---

### Board — List

One-to-Many

Một Board có nhiều List.

Một List chỉ thuộc một Board.

---

### List — Task

One-to-Many

Một List có nhiều Task.

Một Task chỉ nằm trong một List tại một thời điểm.

---

### User — Task

Many-to-Many

Một User có thể được assign nhiều Task.

Một Task có thể được assign cho nhiều User.

---

### Task — Label

Many-to-Many

Một Task có thể có nhiều Label.

Một Label có thể được sử dụng cho nhiều Task.

---

### Task — Comment

One-to-Many

Một Task có nhiều Comment.

Một Comment chỉ thuộc một Task.

---

### Task — Checklist

One-to-Many

Một Task có nhiều Checklist.

Một Checklist chỉ thuộc một Task.

---

### Checklist — Checklist Item

One-to-Many

Một Checklist có nhiều Checklist Item.

Một Checklist Item chỉ thuộc một Checklist.

---

# 22. MVP Requirements

Nếu dùng project này để học Python/FastAPI thì version đầu tiên chỉ cần implement:

1. User có thể register/login.

2. User có thể tạo Workspace.

3. Workspace có thể có nhiều User.

4. User có thể tham gia nhiều Workspace.

5. Workspace có thể có nhiều Board.

6. Board có thể có nhiều User.

7. Board có nhiều List.

8. User có thể tạo, sửa, archive List.

9. List có nhiều Task.

10. User có thể tạo, sửa, archive Task.

11. Task có thể move giữa các List.

12. Task có nhiều trạng thái.

13. Task có Priority.

14. Task có Due Date.

15. Task có thể assign nhiều User.

16. Task có nhiều Label.

17. User có thể Comment vào Task.

18. User có thể filter Task theo:

- status
- priority
- member
- label

19. User chỉ được thao tác trên Workspace/Board mà mình có quyền truy cập.

20. Hệ thống phải lưu đúng relationship và đảm bảo không tạo dữ liệu duplicate không hợp lệ.
