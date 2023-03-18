# Week 0 — Billing and Architecture

10/FEB/2023  
Completed remaining outstanding preparatory steps - all accounts and config steps

11/FEB/2023  
Completed watching livestream on YouTube  
https://www.youtube.com/watch?v=SG8blanhAOg&list=PLBfufR7vyJJ7k25byhRXJldB5AiwgNnWv&index=12

***NOTE: ill for a few days***

16/FEB/2023   
Completed watching Chirag's Week 0 - Spend Considerations (Pricing Basics & Free Tier)  
https://www.youtube.com/watch?v=OVw3RrlP-sI&list=PLBfufR7vyJJ7k25byhRXJldB5AiwgNnWv&index=13  
Study Notes:

AWS Bill Walkthrough
- Root user or IAM user with billing perms
- Pricing varies according to region
- Bills in menu(in USD and local ccy)
- Free Tier in menu - all listed (Current, forecasted usage)

Billing Alerts (CloudWatch Alarm & Budget)
- Billing preference menu
  + Some options
    - PDF invoice by email
    - Fre tier usage alerts
    - Receive billing alerts
    - Clicking on manage billing alert -> (US-East-1) -> CloudWatch -> create alert -> choose options -> SNS topic -> email  
      or  
    - Clicking on Budgets -> Create Budget (Global) -> will alert when threshold of spending crossed (% based)
        
-Cost Explorer
    + Cost Management -> Cost Explorer
    + Cost Management -> Reports

Calculate AWS estimates cost of service
- Pricing - use calc variables (service, instance size, region etc) on the public AWS calculator website then calc a manual estimate 	and compare to the site (730hr vs 744hrs)

Check AWS Credits (voucher)  
Billing -> Credits (redeem if you have)

Cost allocation tags  
Clicking on Cost Alloc Tags -> Activate tags for cost acvitites

Free forever vs free for 12m  
- AWS Free Tier public website
- Filter by Always Free vs 12m free vs trials

18/FEB/2023  
Completed watching Ashish's Week 0 - Security Considerations (AWS Organizations & AWS IAM Tutorial For Beginners)  
https://www.youtube.com/watch?v=4EMWBYVggQI&list=PLBfufR7vyJJ7k25byhRXJldB5AiwgNnWv&index=15  
Study Notes: 
- Cyber Security = Technology risk the business may be exposed to
- Cloud Security = protect data, apps, services in your Cloud envrionments from internal and external security threats
1. Reduce impact of breach
2. Protect networks, apps, services from data theft
3. Reduce human error
Cloud/Cloud security - takes practice due to complexity, new services, threat actors improving capability

Enable MFA for root account - already done!  
- MFA important as compromised domain admin account = game over
- Can double check byu going to main profile -> secruity credentials and review root user config

Create an OU
- Root user account is the management account, recommended it should not have any applications, only used to create ORG / OU
- Example OU strategy = different business units or different environments (eng,dev,uat,prd etc)
- Example account strategy = Active Account OU + Standby Account OU (accounts can take time to create so can cerate in advance in Standby and move into Active as needed)

CloudTrail
- Moniotor data security and residence
- Region vs AZ vs Global
- Audit Logs for IR/Forensice
- Create CloudTrail logs - done

IAM Users
- Create IAM User
- 3 kinds of users in AWS - IAM user, system user, federated user
- Enable MFA for all human users
- Principle of Least Privilege
    
ACtion
- Delete access keys for Root User account - done
- Create IAM user - done
- Enable MFA on newly create IAM user - done

IAM Roles  
2 types off IAM roles & IAM policies - AWS managed vs custom

IAM roles vs IAM policies 
- Role = An IAM role is an identity you can create that has specific permissions with credentials that are valid for short durations. Roles can be assumed by entities that you trust.
- Policy = a group of permissions (ie a role can have inidividual perms assigned but better to use a policy to group up those perms)

Principle of Least Privilege

Create IAM role

Completed Watching Andrew's Follow-Up Video (Generate Credentials, AWS CLI, Budget and Billing Alarm via CLI)  
https://www.youtube.com/watch?v=OdUnNuKylHg&list=PLBfufR7vyJJ7k25byhRXJldB5AiwgNnWv&index=15  
Action:  
Create Budget - done  
Crete Billing Alarm - done

Conceptual Diagram in Lucid:  
https://lucid.app/lucidchart/20d108d1-45e4-46ad-9901-8e1459b7a6d3/edit?view_items=ymoyv3JbMZdO&invitationId=inv_811b50f0-1bc4-4fc6-89f2-b67af0440a82

Logical Diagram in Lucid:  
https://lucid.app/lucidchart/0e4b25fd-2a35-41b3-8992-3d6361ad2211/edit?viewport_loc=-125%2C-19%2C2692%2C1535%2C0_0&invitationId=inv_d783aad2-ec12-405a-a3d3-811c24b5e7d3

23/02/2023  
#To-Do  
- Setup Amazon EventBridge to get Health Dashboard events sent to SNS to email me when there is a service health issue
- Connect AWS access keys to VSCode for CLI commands (already setup AWS CLI in GitPod)
- Open support ticket to increae limit of elastic IP
