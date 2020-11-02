from django.test import TestCase, Client
from django.contrib import auth
from django.db import models
from .models import Profile, ProfileManager, FriendRequest
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from .filters import DropdownFilter


class AuthenticationTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test', password='password')
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test_correct(self):
        user = authenticate(username='test', password='password')
        self.assertTrue((user is not None) and user.is_authenticated)

    def test_wrong_username(self):
        user = authenticate(username='wrong', password='password')
        self.assertFalse(user is not None and user.is_authenticated)

    def test_wrong_pssword(self):
        user = authenticate(username='test', password='wrongpassword')
        self.assertFalse(user is not None and user.is_authenticated)


class ProfileModelsTest(TestCase):

    def setUp(self):
        self.testUser = User(username='testUser', password='password')
        self.testUser.save()
        self.testProfile = Profile.objects.get(user=self.testUser)

    def tearDown(self):
        self.testUser.delete()

    def testNewProfile(self):
        self.assertTrue(self.testProfile.name == None)
        self.assertTrue(self.testUser.username == "testUser")
        self.assertTrue(self.testProfile.image == "default.jpg")
        self.assertTrue(self.testProfile.phone == None)
        self.assertTrue(self.testProfile.major == '')
        self.assertTrue(self.testProfile.minor == '')
        self.assertTrue(self.testProfile.graduation == '')
        self.assertTrue(self.testProfile.gender == '')
        self.assertTrue(self.testProfile.age == None)
        self.assertTrue(self.testProfile.zoom_link == '')


class FriendListTest(TestCase):

    def setUp(self):
        self.testUser1 = User(username='testUser1', password='password')
        self.testUser2 = User(username='testUser2', password='password')
        self.testUser3 = User(username='testUser3', password='password')
        self.testUser1.save()
        self.testUser2.save()
        self.testUser3.save()
        FriendRequest.objects.get_or_create(from_user=self.testUser2, to_user=self.testUser3)

    def tearDown(self):
        self.testUser1.delete()
        self.testUser2.delete()
        self.testUser3.delete()

    def testFriendRequestDNE(self):
        try:
            FriendRequest.objects.get(from_user=self.testUser1, to_user=self.testUser2)
            test_code = 0
        except:
            test_code = 1
        self.assertEquals(test_code, 1)

    def testSendFriendRequest(self):
        try:
            FriendRequest.objects.get(from_user=self.testUser2, to_user=self.testUser3)
            test_code = 0
        except:
            test_code = 1
        self.assertEquals(test_code, 0)

        try:
            FriendRequest.objects.get(from_user=self.testUser3, to_user=self.testUser2)
            test_code = 0
        except:
            test_code = 1
        self.assertEquals(test_code, 1)

    def testCancelFriendRequest(self):
        frequest = FriendRequest.objects.get(from_user=self.testUser2, to_user=self.testUser3)
        frequest.delete()
        try:
            FriendRequest.objects.get(from_user=self.testUser2, to_user=self.testUser3)
            test_code = 0
        except:
            test_code = 1
        self.assertEquals(test_code, 1)

    def testAcceptFriendRequest(self):
        # Accept Friend Request
        profile1 = Profile.objects.get(user=self.testUser3)
        profile2 = Profile.objects.get(id=self.testUser2.id)
        frequest = FriendRequest.objects.get(from_user=profile2.user, to_user=self.testUser3)
        profile1.friends.add(profile2)
        profile2.friends.add(profile1)
        frequest.delete()

        # Test friend request was deleted
        try:
            FriendRequest.objects.get(from_user=self.testUser2, to_user=self.testUser3)
            test_code = 0
        except:
            test_code = 1
        self.assertEquals(test_code, 1)

        # Test friend exists in profile
        prof2 = ([profile for profile in Profile.objects.get(user=self.testUser3).friends.all()][0])
        self.assertEquals(prof2, Profile.objects.get(user=self.testUser2))

        prof3 = ([profile for profile in Profile.objects.get(user=self.testUser2).friends.all()][0])
        self.assertEquals(prof3, Profile.objects.get(user=self.testUser3))

    def testRemoveFriend(self):
        # Accept Friend
        profile1 = Profile.objects.get(user=self.testUser3)
        profile2 = Profile.objects.get(id=self.testUser2.id)
        frequest = FriendRequest.objects.get(from_user=profile2.user, to_user=self.testUser3)
        profile1.friends.add(profile2)
        profile2.friends.add(profile1)
        frequest.delete()

        # Remove friends
        profile1.friends.remove(profile2)
        profile2.friends.remove(profile1)

        prof2 = ([profile for profile in Profile.objects.get(user=self.testUser3).friends.all()])
        self.assertEquals(prof2, [])

        prof3 = ([profile for profile in Profile.objects.get(user=self.testUser2).friends.all()])
        self.assertEquals(prof3, [])


class FilterTestCase(TestCase):

    def setUp(self):
        self.testUser1 = User(username='testUser1', password='password')
        self.testUser2 = User(username='testUser2', password='password')
        self.testUser3 = User(username='testUser3', password='password')
        self.testUser4 = User(username='testUser4', password='password')
        self.testUser5 = User(username='testUser5', password='password')
        self.testUser1.save()
        self.testUser2.save()
        self.testUser3.save()
        self.testUser4.save()
        self.testUser5.save()

        f = Profile.objects.get(user=self.testUser1)
        setattr(f, 'name', 'Daniel')
        setattr(f, 'gender', 'Male')
        setattr(f, 'major', 'Archaeology')
        setattr(f, 'minor', 'Computer Science')
        setattr(f, 'graduation', '2022')
        setattr(f, 'age', 22)
        setattr(f, 'zoom_link', 'https://zoom.com')
        f.save()

        f1 = Profile.objects.get(user=self.testUser2)
        setattr(f1, 'name', 'Water')
        setattr(f1, 'major', 'Commerce')
        setattr(f1, 'graduation', '2021')
        f1.save()

        f2 = Profile.objects.get(user=self.testUser3)
        setattr(f2, 'name', 'user3')
        setattr(f2, 'major', 'Politics')
        setattr(f2, 'graduation', '2025')
        f2.save()

        f3 = Profile.objects.get(user=self.testUser4)
        setattr(f3, 'name', 'user3')
        setattr(f3, 'major', 'Politics')
        setattr(f3, 'graduation', '2025')
        f3.save()

        f4 = Profile.objects.get(user=self.testUser5)
        setattr(f4, 'name', 'user5')
        setattr(f4, 'major', 'Sociology')
        setattr(f4, 'graduation', '2024')
        f4.save()

        self.profile1 = Profile.objects.get(user=self.testUser1)
        self.profile2 = Profile.objects.get(user=self.testUser2)
        self.profile3 = Profile.objects.get(user=self.testUser3)
        self.profile4 = Profile.objects.get(user=self.testUser4)
        self.profile5 = Profile.objects.get(user=self.testUser5)

    def testMajorFilter(self):
        qs = Profile.objects.all()

        f = DropdownFilter(data={'major': 'Commerce'}, queryset=qs)
        result = f.qs
        self.assertEquals(result.first(), self.profile2)

        f1 = DropdownFilter(data={'major': 'Archaeology'}, queryset=qs)
        result = f1.qs
        self.assertEquals(result.first(), self.profile1)

    def testMajorFilterMultiple(self):
        qs = Profile.objects.all()

        f = DropdownFilter(data={'major': 'Politics'}, queryset=qs)
        result = f.qs
        match_set = {result.first(), result.last()}
        profile_set = {self.profile3, self.profile4}
        self.assertEquals(match_set, profile_set)

    def testGraduationFilter(self):
        qs = Profile.objects.all()

        f = DropdownFilter(data={'graduation': '2022'}, queryset=qs)
        result = f.qs
        self.assertEquals(result.first(), self.profile1)

        f = DropdownFilter(data={'graduation': '2021'}, queryset=qs)
        result = f.qs
        self.assertEquals(result.first(), self.profile2)

    def testGraduationFilterMultiple(self):
        qs = Profile.objects.all()

        f = DropdownFilter(data={'graduation': '2025'}, queryset=qs)
        result = f.qs
        match_set = {result.first(), result.last()}
        profile_set = {self.profile3, self.profile4}
        self.assertEquals(match_set, profile_set)

    def testNameFilter(self):
        qs = Profile.objects.all()

        f = DropdownFilter(data={'name': 'Daniel'}, queryset=qs)
        result = f.qs
        self.assertEquals(result.first(), self.profile1)

        f = DropdownFilter(data={'name': 'Water'}, queryset=qs)
        result = f.qs
        self.assertEquals(result.first(), self.profile2)

    def testNameFilterMultiple(self):
        qs = Profile.objects.all()

        f = DropdownFilter(data={'name': 'user3'}, queryset=qs)
        result = f.qs
        match_set = {result.first(), result.last()}
        profile_set = {self.profile3, self.profile4}
        self.assertEquals(match_set, profile_set)

    def testNoMatch(self):
        qs = Profile.objects.all()

        f = DropdownFilter(data={'major': 'Religious Studies'}, queryset=qs)
        result = f.qs
        match_list = list(result)
        profile_list = []
        self.assertEquals(match_list, profile_list)