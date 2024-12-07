from mongoDb import mongoDb
from objects import *
import pytest
import utils
from AppConfig import AppConfig

db = mongoDb()

def createUserObject(userId, email='test@gmail.com', roles={}):
    return {
        '_id': userId,
        '_version': 0,
        'roles': roles,
        'createdAt': datetime.datetime.now(),
        'isApproved': True,
        'email': email,
        'image': 'testImage',
        'displayName': 'testDisplayName',
    }

userObject = createUserObject(None, 'superAdmin@gmail.com')

userObject2 = createUserObject(None, 'user@gmail.com')

offenseObject = {
    '_id': None,
    'number': 0,
    'description': 'description',
    'remedialActions': ['Verbal Warning', 'Written Warning', 'Suspension', 'Termination'],
    '_version': 0
}

employeeObject = {
    '_id': None,
    'name': 'name',
    'email': 'email',
    'address': 'address',
    'phoneNumber': 'phone',
    'photoOfPerson': 'photoOfPerson',
    'resumePhotosList': ['resumePhotosList'],
    'biodataPhotosList': ['biodataPhotosList'],
    'dateJoined': datetime.datetime.now(),
    'company': 'Pustanan',
    'isRegular': True,
    'isProductionEmployee': True,
    'dailyWage': None,
    '_version': 0
}

memoObject = {
    '_id': None,
    'mediaList': ['mediaList'],
    'Employee': employeeObject,
    'memoPhotosList': ['memoPhotosList'],
    'subject': 'subject',
    'MemoCode': offenseObject,
    'submitted': False,
    'description': 'description',
    'date': datetime.datetime.now(),
    'reason': None,
    '_version': 0
}

def test_user_login():
    try:
        db.delete({},'User')
        # userObject['_id'] = 123
        user = UserActions(userObject)

        userCreated = user.createFirstUserAction('id1')

        firstUser = db.read({'_id':userCreated['_id']},'User',findOne=True)

        assert firstUser['email'] == userCreated['email']
    finally:
        db.delete({},'User')
        pass

def test_duplicate_user_creation():
    try:
        user = UserActions(userObject)
        user.createFirstUserAction('id1')

        users = user.readCollection('User')

        assert len(users) == 1

        with pytest.raises(ValueError, match='Cannot create first user. First user already exist in the system.'):
            user.createFirstUserAction('id1')
    finally:
        db.delete({}, 'User')

def test_add_role_and_remove_role():
    try:
        # create first user
        user = UserActions(userObject)
        firstUser = user.createFirstUserAction('id1')


        user2 = UserActions(userObject)
        userCreated = user2.createUserAction('id2')

        users = user2.readCollection('User')

        assert len(users) == 2

        addRole = user.addRoleAction(users[1], 'Memo', 'canCreateMemo')

        addRole2 = user.addRoleAction(users[1], 'Memo', 'canDeleteMemo')

        with pytest.raises(ValueError, match='Role already exists'):
            addRole3 = user.addRoleAction(users[1], 'Memo', 'canCreateMemo')

        with pytest.raises(ValueError, match='Role does not exist in category'):
            addRole4 = user.addRoleAction(users[1], 'Memo', 'noRole')

        assert addRole[0]['roles']['Memo'][0] == 'canCreateMemo'
        userWithRole = db.read({'_id':users[0]['_id']},'User',findOne=True)
        assert 'canCreateMemo' in userWithRole['roles']['Memo']

        user3 = UserActions(userObject2)
        userCreated = user3.createUserAction('id3')

        users = user3.readCollection('User')

        assert len(users) == 3

        removeRole = user3.removeRoleAction(users[1],'Memo', 'canCreateMemo')

        assert len(removeRole[0]['roles']['Memo']) == 1
        user = db.read({'_id':users[1]['_id']},'User',findOne=True)
        assert 'canCreateMemo' not in user['roles']['Memo']
    finally:
        db.delete({},'User')
        pass

def test_create_offense_employee_memo():
    try:
        user = UserActions(userObject)
        userCreated = user.createFirstUserAction('id4')

        offense = user.createOffenseAction(userCreated, offenseObject)

        offenses = user.readCollection('Offense')

        assert offense['number'] == offenses[0]['number']

        getOffense = db.read({'_id':offenses[0]['_id']},'Offense',findOne=True)

        assert getOffense['remedialActions'][0] == offense['remedialActions'][0]

        # create employee
        employee = user.createEmployeeAction(userCreated, employeeObject)
        print(employee)
        employees = user.readCollection('Employee')

        getEmployee = db.read({'_id':employees[0]['_id']},'Employee',findOne=True)

        assert getEmployee['name'] == employee['name']

        # create memo
        memo = user.createMemoAction(userCreated, memoObject)

        memos = user.readCollection('Memo')

        getMemo = db.read({'_id':memos[0]['_id']},'Memo',findOne=True)

        assert getMemo['subject'] == memo['subject']

        # create another memo
        memo2 = user.createMemoAction(userCreated, memoObject)

        memos = user.readCollection('Memo')

        # create another memo then submit it
        memo3 = user.createMemoAction(userCreated, memoObject)

        reason = 'Reason for submission'

        submitMemo = user.submitMemoAction(userCreated, memo3, reason)

        getMemo = db.read({'_id':submitMemo[0]['_id']},'Memo',findOne=True)

        assert getMemo['submitted'] == True

        memos = user.readCollection('Memo')

        memo4 = user.createMemoAction(userCreated, memoObject)

        reason = 'Reason for submission'

        submitMemo = user.submitMemoAction(userCreated, memo4, reason)

        getMemo = db.read({'_id':submitMemo[0]['_id']},'Memo',findOne=True)

        assert getMemo['submitted'] == True

        memos = user.readCollection('Memo')

        assert len(memos) == 4

    finally:
        db.delete({},'User')
        db.delete({},'Offense')
        db.delete({},'Employee')
        db.delete({},'Memo')
        pass

def test_update_offense():
    try:
        user = UserActions(userObject)
        userCreated = user.createFirstUserAction('id5')

        offense = user.createOffenseAction(userCreated, offenseObject)

        getOffense = db.read({'_id':offense['_id']},'Offense',findOne=True)

        assert getOffense['number'] == offense['number']

        updateOffense = user.updateOffenseAction(userCreated, offense, {'number':'number2'})

        getOffense = db.read({'_id':updateOffense[0]['_id']},'Offense',findOne=True)

        assert getOffense['number'] == 'number2'
    finally:
        db.delete({},'User')
        db.delete({},'Offense')
        pass

def test_delete_offense():
    try:
        user = UserActions(userObject)
        userCreated = user.createFirstUserAction('id6')

        offense = user.createOffenseAction(userCreated, offenseObject)

        getOffense = db.read({'_id':offense['_id']},'Offense',findOne=True)

        assert getOffense['number'] == offense['number']

        deleteOffense = user.deleteOffenseAction(userCreated, getOffense)

        offenses = user.readCollection('Offense')

        assert len(offenses) == 0
    finally:
        db.delete({},'User')
        db.delete({},'Offense')
        pass

def test_create_update_delete_employee():
    try:
        user = UserActions(userObject)
        userCreated = user.createFirstUserAction('id7')

        employee = user.createEmployeeAction(userCreated ,employeeObject)

        employeeDashboard = user.getEmployeeForDashboardAction(userCreated)

        assert len(employeeDashboard) == 1

        getEmployee = db.read({'_id':employee['_id']},'Employee',findOne=True)

        assert getEmployee['name'] == employee['name']

        updateEmployee = user.updateEmployeeAction( userCreated, employee, {'name':'name2'})

        getEmployee = db.read({'_id':updateEmployee[0]['_id']},'Employee',findOne=True)

        assert getEmployee['name'] == 'name2'

        deleteEmployee = user.deleteEmployeeAction(userCreated, getEmployee)

        employees = user.readCollection('Employee')

        assert len(employees) == 0

        employeeDashboard = user.getEmployeeForDashboardAction(userCreated)

        assert len(employeeDashboard) == 0

    finally:
        db.delete({},'User')
        db.delete({},'Employee')
        pass

def test_submit_and_delete_memo():
    try:
        user = UserActions(userObject)
        userCreated = user.createFirstUserAction('id8')

        memo = user.createMemoAction(userCreated ,memoObject)

        getMemo = db.read({'_id':memo['_id']},'Memo',findOne=True)

        assert getMemo['subject'] == memo['subject']

        reason = 'Reason for submission'

        memoToSubmit = user.getAllMemoThatsNotSubmittedAction(userCreated)

        assert len(memoToSubmit) == 1

        submitMemo = user.submitMemoAction(userCreated, memo, reason)

        getMemo = db.read({'_id':submitMemo[0]['_id']},'Memo',findOne=True)

        assert getMemo['submitted'] == True

        with pytest.raises(ValueError, match='Memo has already been submitted'):
            deleteMemo = user.deleteMemoAction(userCreated, getMemo)

        memo2 = user.createMemoAction(userCreated, memoObject)

        getMemo2 = db.read({'_id':memo2['_id']},'Memo',findOne=True)

        assert getMemo2['subject'] == memo2['subject']

        deleteMemo = user.deleteMemoAction(userCreated, getMemo2)

        memos = user.readCollection('Memo')

        assert len(memos) == 1

        memoList = user.getMemoListAction(userCreated, memos[0]['Employee']['_id'])

        assert len(memoList) == 1

    finally:
        db.delete({},'User')
        db.delete({},'Memo')
        pass

def test_submit_memo_without_reason():
    try:
        user = UserActions(userObject)
        userCreated = user.createFirstUserAction('id1')
        memo = user.createMemoAction(userCreated, memoObject)

        with pytest.raises(ValueError, match='Reason must be provided'):
            user.submitMemoAction(userCreated, memo, None)
    finally:
        db.delete({}, 'User')
        db.delete({}, 'Memo')

def test_delete_non_existent_offense():
    try:
        user = UserActions(userObject)
        userCreated = user.createFirstUserAction('id1')

        offenseObject = {
            '_id': None,
            'number': 0,
            'description': 'description',
            'remedialActions': ['Verbal Warning', 'Written Warning', 'Suspension', 'Termination'],
            '_version': 0
        }

        with pytest.raises(ValueError, match='Offense does not exist'):
            user.deleteOffenseAction(userCreated, offenseObject)
    finally:
        db.delete({}, 'User')
        db.delete({}, 'Offense')


if __name__ == '__main__':
    if AppConfig().getIsProductionEnvironment():
        raise ValueError('Not to be run in cloud production environment')
    # test_user_login()
    # test_duplicate_user_creation()
    # test_add_role_and_remove_role()
    # test_create_offense_employee_memo()
    # test_update_offense()
    # test_delete_offense()
    # test_create_update_delete_employee()
    test_submit_and_delete_memo()
    # test_submit_memo_without_reason()
    # test_delete_non_existent_offense()
    pass
