from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from .models import VerificationCode, User
from utils.function_utils import check_ip_block, generate_verification_code


@csrf_exempt
def request_verification(request):
    ip_address = request.META.get('REMOTE_ADDR')
    phone_number = request.POST.get('phone_number')
    
    if User.objects.filter(phone_number=phone_number).exists():
        return JsonResponse({'message': 'User with this phone number exists. please login'})

    try:
        code_entry, created = VerificationCode.objects.get_or_create(
            phone_number=phone_number,
            ip_address=ip_address
        )
        
        # Check blocking
        if check_ip_block(ip_address, VerificationCode):
            return JsonResponse({'error': 'You are blocked for an hour.'}, status=403)
        else:
            code_entry.code = generate_verification_code()
            # Reset attempts
            if code_entry.attempts >= 3:
                code_entry.attempts = 0
            code_entry.save()
        if not created: 
            try:
                # Check phone validator and increase attempts and update last attempt time
                code_entry.full_clean()
                code_entry.attempts += 1
                code_entry.last_attempt = timezone.now()
                code_entry.save()
            except ValidationError as e:
                error_message = e.message_dict.get('phone_number', ['Invalid input'])[0]
                return JsonResponse({'error': error_message}, status=400)
                    
        return JsonResponse({'message': 'Verification code sent successfully',
                             'code': code_entry.code})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def verify_code(request):
    phone_number = request.POST.get('phone_number')
    code = request.POST.get('code')
    ip_address = request.META.get('REMOTE_ADDR')
    
    try:
        code_entry = VerificationCode.objects.get(phone_number=phone_number, ip_address=ip_address)
        code_entries = VerificationCode.objects.filter(phone_number=phone_number)
        
        # Check one phone number with multiple IPs
        if len(code_entries) > 1:
            code_entry.attempts += 1
            code_entry.last_attempt = timezone.now()
            code_entry.save()
        
        if check_ip_block(ip_address, VerificationCode):
            return JsonResponse({'error': 'You are blocked for an hour.'}, status=403)
        else:
            if code_entry.attempts >= 3:
                code_entry.attempts = 0
                code_entry.save()
                
        if code_entry.code == code:
            # Create session for register and remove verification object
            request.session['phone_number'] = phone_number
            code_entry.delete()
            return JsonResponse({'message': 'Phone number verified successfully'})
        else:
            # Check phone validator and increase attempts and update last attempt time
            code_entry.attempts += 1
            code_entry.last_attempt = timezone.now()
            code_entry.save()
            return JsonResponse({'error': 'Incorrect verification code'}, status=400)
        
    except VerificationCode.DoesNotExist:
        return JsonResponse({'error': 'Verification code not requested'}, status=400)


@csrf_exempt
def complete_registration(request):
    phone_number = request.session.get('phone_number')
    ip_address = request.META.get('REMOTE_ADDR')
    if not phone_number:
        return JsonResponse({'error': 'Phone number verification is required'}, status=403)
    
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    email = request.POST.get('email')
    password = request.POST.get('password')

    if not all([first_name, last_name, email, password]):
        return JsonResponse({'error': 'All fields are required'}, status=400)

    if User.objects.filter(email=email).exists():
        return JsonResponse({'error': 'This email is already registered'}, status=400)

    user = User(
        phone_number=phone_number,
        first_name=first_name,
        last_name=last_name,
        email=email,
        ip_address=ip_address
    )
    
    try:
        # Check phone validation and create user
        user = User(
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
            email=email,
            ip_address=ip_address
        )
        user.set_password(password)
        user.full_clean()
        user.save()
    except ValidationError as e:
        return JsonResponse({'error': str(e)}, status=400)
    del request.session['phone_number']
    return JsonResponse({'message': 'Registration complete and logged in successfully'})


@csrf_exempt
def login(request):
    ip_address = request.META.get('REMOTE_ADDR')
    phone_number = request.POST.get('phone_number')
    password = request.POST.get('password')
    
    try:
        user = User.objects.get(phone_number=phone_number)

        # Check blocking for password entry
        if check_ip_block(ip_address, User):
            return JsonResponse({'error': 'You are blocked for an hour.'}, status=403)
        else:
            if user.attempts >= 3:
                user.attempts = 0
                user.save()
        if user.check_password(password):
            return JsonResponse({'message': 'Login successful'})
        else:
            # Increase attempts for wrong password
            user.attempts += 1
            user.last_attempt = timezone.now()
            user.save()
            return JsonResponse({'error': 'Incorrect password'}, status=400)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

