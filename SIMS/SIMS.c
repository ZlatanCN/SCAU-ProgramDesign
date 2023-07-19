
#include <stdio.h>
#include <stdlib.h>
#include <conio.h>
#include <string.h>

typedef struct StuID
{
	//学生证信息内的8种数据 
	char name[10];			//姓名 
	char sex[5];			//性别 
	char date[15];			//入学年月日（2022年9月1日） 
	char num[20];				//学号 
	int years;				//学制 
	char cleg[30];			//学院 
	char clas[30];			//班级
	char cnum[10];			//班级编号 
	//指向下个节点的指针
	struct StuID *next;
}SID;

SID *ph = NULL;

SID *seenum(char *num);
SID *seecnum(char *cnum);
int readf();
void menu();
int create();
int search();
int modify();
int del();
int savef();
int count();

int main()
{
	ph = NULL;
	if(readf())
	{
		printf("初始化成功，欢迎使用学生证信息管理系统！\n");
	}
	else
	{
		printf("未发现文件！请在本程序所属目录新建studata.txt再重启程序！\n");
		printf("输入任意键退出");
		getchar();
		return 0;
	}
	while(1)
	{
		int choice;
		menu();
		scanf("%d",&choice);
		switch(choice)
		{
			case 1:
				system("cls");
				printf("====================新建学生证信息====================\n");
				if(create())
				{
					printf("新建信息成功\n");
				}
				else
				{
					printf("新建信息失败\n");
				}
				break;
			case 2:
				system("cls");
				printf("====================查询学生证信息====================\n");
				search();
				break;
			case 3:
				system("cls");
				printf("====================修改学生证信息====================\n");
				if(modify())
				{
					break;
				}
			case 4:
				system("cls");
				printf("====================删除学生证信息====================\n");
				if(del())
				{
					printf("删除成功！\n\n");
					break;
				}
				else
				{
					printf("不存在此学号的信息！\n\n");
					break;
				}
			case 5:
				system("cls");
				printf("====================统计学生证信息====================\n");
				count();
				break;
			case 0:
				system("cls");
				printf("======================================================\n");
				if(savef())
				{
					printf("信息保存成功\n\n");
				}
				else
				{
					printf("信息保存失败\n\n");
				}
				printf("再见！");
				if(!ph)
				{
					free(ph);
				}
				printf("按任意键结束程序：");
				getch();
				return 0;
		}		
	} 
}

int readf()
{
	FILE *st = fopen("studata.txt","r");
	SID *p,*tail;
	if(!st)
	{
		return 0;
	}
	fgetc(st);	//读取文件内的值，光标移动到下一个位置 
	if(!feof(st))
	{
		rewind(st);
	}
	while(!feof(st))	//当文件未结束时 
	{
		
		p = (SID*)malloc(sizeof(SID));
		fscanf(st,"%s\n%s\n%s\n%s\n%d\n%s\n%s %s",p->num,p->name,p->sex,p->date,&p->years,p->cleg,p->clas,p->cnum);	//插入数据 
		if(ph == NULL)
		{
			ph = p;
			tail = p;
		}
		else
		{
			tail->next = p;
			tail = p;
		}
		fgetc(st);
		fgetc(st);	//连续用两次以读取汉字 
		if(feof(st))
		{
			tail->next = NULL;
		}
	}
	if(!st)
	{
		fclose(st);
	}
	return 1;
}

void menu()
{
  printf("◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆\n\n");
	printf("					1.新建学生证信息\n\n");
	printf("					2.查询学生证信息\n\n");
	printf("					3.修改学生证信息\n\n");
	printf("					4.删除学生证信息\n\n");
	printf("                                        5.统计学生证信息\n\n");
	printf("					0.保存并退出系统\n\n");
	printf("◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆◇◆\n\n");
	printf("请选择您要进行的操作：");
}

SID *seenum(char *num)
{
	SID *p;
	p = ph;
	while(p && strcmp(num,p->num))
	{
		p = p->next;
	}
	return p;	//到最后都没找到则返回NULL 
}

SID *seecnum(char *cnum)
{
	SID *p;
	p = ph;
	while(p && strcmp(cnum,p->cnum))
	{
		p = p->next;
	}
	return p;
}

int create()
{
	SID *p,*head,*tail;
	int a = 1;
	head = NULL;
	do
	{
		p = (SID*)malloc(sizeof(SID));
		printf("请输入学号：");
		scanf("%s",p->num);
		if(seenum(p->num))	//查询是否已录入该学生证信息 
		{
			printf("已存在学号为%s的学生证信息！\n",p->num);
			return 0;
		}
		printf("请输入姓名：");
		scanf("%s",p->name);
		printf("请输入性别：") ;
		scanf("%s",p->sex);
		printf("请输入入学日期（例：2022年9月1日）：");
		scanf("%s",p->date);
		printf("请输入学制：");
		scanf("%d",&p->years);
		printf("请输入学院：");
		scanf("%s",p->cleg);
		printf("请输入班级和班级编号：");
		scanf("%s",p->clas);
		scanf("%s",p->cnum);
		if(head == NULL)
		{
			head = p;
			tail = p;
		}
		else
		{
			tail->next = p;
			tail = p;
		}
		tail->next = NULL;
		printf("\n输入0回车终止新建，输入其他数字继续新建：");
		scanf("%d",&a);
		printf("\n"); 
	}
	while(a != 0);
	//根据head与ph的状态连接链表 
	if(head)	//head不为空 
	{
		if(ph)	//ph不为空 
		{
			tail->next = ph;
			ph = head;
			return 1;
		}
		else	//ph为空 
		{
			ph = head;
			return 1;
		}
	}
	else	//head为空 
	{
		return 0;
	}
}

int search()	//输入学号返回个人信息，输入班级编号返回所有学生的信息 
{
	SID *p;
	int choice = 0;
	char n[20];
	char cn[10];
	while(choice != 1 && choice != 2)
	{
		printf("1.按学号查找\n2.按班级查找\n请选择您的操作：");
		scanf("%d",&choice);
		printf("\n"); 
	}
	if(choice == 1)
	{
		printf("请输入该学生的学号：");
		scanf("%s",n);
		SID *temp = ph;
		printf("======================================================\n");
		if(seenum(n))	//查找有无此学号 
		{
			while(temp)
			{
				if(strcmp(temp->num,n) == 0)
				{
					printf("学号：%s\n姓名：%s\n性别：%s\n入学日期：%s\n学制：%d\n学院：%s\n班级和班级编号：%s %s\n",
				 			 temp->num,temp->name,temp->sex,temp->date,temp->years,temp->cleg,temp->clas,temp->cnum);
				 	break;
				}
				temp = temp->next;
			}
		}
		else
		{
			printf("查无此人");
		}
		printf("\n");
	}
	if(choice == 2)
	{
		printf("请输入该班级的班级编号：");
		scanf("%s",cn);
		printf("======================================================\n");
		SID *temp = ph;
		if(seecnum(cn))	//查找有无此班级编号 
		{
			while(temp)
			{
				if(strcmp(temp->cnum,cn) == 0)	//比较字符串是否相等 
				{
					printf("学号：%s\n姓名：%s\n性别：%s\n入学日期：%s\n学制：%d\n学院：%s\n班级和班级编号：%s %s\n",
				 			 temp->num,temp->name,temp->sex,temp->date,temp->years,temp->cleg,temp->clas,temp->cnum);
				 	printf("------------------------------------------------------\n");
				}
				temp = temp->next;
			}
		}
		else
		{
			printf("查无此班\n");
		}
	}
	getchar();
	printf("输入任意键回车返回主页：");
	getchar();
	printf("\n");
}

int modify()
{
	printf("请输入您要修改的学生学号：");
	char n[20];
	int choice,rechoice;
	SID *temp = ph; 
	scanf("%s",n);
	if(seenum(n))
	{
		while(temp)
		{
			if(strcmp(temp->num,n) == 0)
			{
				printf("1.学号：%s\n2.姓名：%s\n3.性别：%s\n4.入学日期：%s\n5.学制：%d\n6.学院：%s\n7.班级和班级编号：%s %s\n",
			 			 temp->num,temp->name,temp->sex,temp->date,temp->years,temp->cleg,temp->clas,temp->cnum);
			 	break;
			}
			temp = temp->next;
		}
		do
		{
			printf("\n请选择您要修改的序号：");
			scanf("%d",&choice);
			switch(choice)
			{
				case 1:
					printf("请输入新的学号：");
					scanf("%s",temp->num);
					break;
				case 2:
					printf("请输入新的姓名：");
					scanf("%s",temp->name);
					break;
				case 3:
					printf("请输入新的性别：");
					scanf("%s",temp->sex);
					break;
				case 4:
					printf("请输入新的入学日期（例：2022年9月1日）：");
					scanf("%s",temp->date);
					break;
				case 5:
					printf("请输入新的学制：");
					scanf("%d",&temp->years);
					break;
				case 6:
					printf("请输入新的学院：");
					scanf("%s",temp->cleg);
					break;
				case 7:
					printf("请输入新的班级和班级编号：");
					scanf("%s%s",temp->clas,temp->cnum);
					break;
			}
			printf("\n输入0回车返回主页，输入其他数字回车继续修改："); 
			scanf("%d",&rechoice);
		}
		while(rechoice != 0);
		printf("\n修改成功！");
	}
	else
	{
		printf("不存在此学号的记录！\n");
		return 1; 
	}
}

int del()
{
	SID *temp = ph,*pretemp;
	char n[20];
	printf("请输入您要删除的学生信息的学号：");
	scanf("%s",n);
	if((!(seenum(n))) && (!temp))
	{
		return 0;
	}
	if(strcmp(temp->num,n) == 0)	//当删除的是头结点时 
	{
		if(!temp->next)	//当头节点之后没有数据时 
		{
			ph = NULL;
			free(temp);
			return 1;
		}
		else
		{
			ph = temp->next;
			free(temp);
			return 1;
		}
	}
	while(strcmp(temp->num,n) != 0)
	{
		pretemp = temp;
		temp = temp->next;	//结束循环后，temp指向该学生；pretemp指向前一个学生 
	}
	pretemp->next = temp->next;	//连接被删除学生的下一个节点 
	free(temp);
	return 1;
}

int savef()
{
	FILE *st = fopen("studata.txt","w");
	SID *p;
	if(!st)
	{
		return 0;
	}
	p = ph;
	while(p)
	{
		fprintf(st,"%s\n%s\n%s\n%s\n%d\n%s\n%s %s\n\n",
					p->num,p->name,p->sex,p->date,p->years,p->cleg,p->clas,p->cnum);
					p = p->next;
	}
	if(!st)
	{
		fclose(st);
	}
	return 1;
}

int count()
{
	SID *temp = ph;
	char grad[8]; 
	char cleg[30];
	char major[30];
	char cnum[10];
	printf("1.班级人数\n\n");
	printf("2.专业人数\n\n");
	printf("3.学院人数\n\n");
	printf("4.年级人数\n\n");
	printf("5.学生人数\n\n");
	printf("======================================================\n");
	printf("请选择您的操作：");
	int choice;
	scanf("%d",&choice);
	switch(choice)
	{
		case 1:
			printf("请输入班级编号：");
			scanf("%s",cnum); 
			int i = 0;
			while(temp)
			{
				if(strcmp(cnum,temp->cnum) == 0)
				{
					i++;
				}
				temp = temp->next;
			}
			printf("该班级学生人数为：%d\n",i);
			break;
		case 2:
			printf("请输入专业全称：");
			scanf("%s",major); 
			int a = 0;
			while(temp)
			{
				if(strstr(temp->clas,major) != NULL)
				{
					a++;
				}
				temp = temp->next;
			} 
			printf("该专业学生人数为：%d\n",a);
			break;
		case 3:
			printf("请输入学院全称：");
			scanf("%s",cleg);
			int j = 0;
			while(temp)
			{
				if(strcmp(cleg,temp->cleg) == 0)
				{
					j++;
				}
				temp = temp->next;
			}
			printf("该学院学生人数为：%d\n",j);
			break;
		case 4:
			printf("请输入入学年份（例：2022）：");
			scanf("%s",grad);
			int k = 0;
			while(temp)
			{
				if(grad[0] == temp->date[0] && grad[1] == temp->date[1] && grad[2] == temp->date[2] &&grad[3] == temp->date[3])
				{
					k++;
				}
				temp = temp->next;
			}
			printf("该年级学生人数为：%d\n",k);
			break;
		case 5:
			printf("已录入信息的学生人数为：");
			int b = 0;
			while(temp)
			{
				b++;
				temp = temp->next;
			}
			printf("%d\n",b-1);
			break;
	}
}
